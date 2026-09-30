import http.server
import socketserver
import json
import urllib.parse
import os
import mimetypes
from database import get_connection, create_order, approve_order, get_orders, verify_token
from mailer import send_ebook_email

PORT = int(os.environ.get("PORT", 8000))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class EbookRequestHandler(http.server.BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # 1. 메인 랜딩 페이지
        if path == "/" or path == "/index.html":
            self.serve_file(os.path.join(BASE_DIR, "landing_page.html"), "text/html; charset=utf-8")
            return

        # 2. 정적 파일 (cover.jpg 등)
        if path == "/cover.jpg":
            self.serve_file(os.path.join(BASE_DIR, "cover.jpg"), "image/jpeg")
            return

        # 3. 도서 메타데이터 API (외부 사이트 연동용)
        if path == "/api/meta":
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM book_meta LIMIT 1")
            row = cur.fetchone()
            conn.close()
            data = dict(row) if row else {}
            self.send_json(200, data)
            return

        # 4. 주문 목록 조회 API (관리자용)
        if path == "/api/orders":
            orders = get_orders()
            self.send_json(200, {"orders": orders})
            return

        # 5. 관리자 대시보드
        if path == "/admin":
            self.serve_admin_dashboard()
            return

        # 6. 임베드 위젯 페이지 (외부 사이트 iframe용)
        if path == "/widget":
            self.serve_file(os.path.join(BASE_DIR, "embed_widget.html"), "text/html; charset=utf-8")
            return

        # 7. PDF 직접 다운로드 (보안 토큰 인증)
        if path == "/download":
            token = query.get("token", [""])[0]
            order = verify_token(token)
            if not order:
                self.send_response(403)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("<h3>[접근 거부] 유효하지 않거나 미입금 상태인 다운로드 링크입니다.</h3>".encode("utf-8"))
                return
            
            pdf_path = os.path.join(BASE_DIR, "ebook_final.pdf")
            if not os.path.exists(pdf_path):
                self.send_error(404, "PDF File Not Found")
                return

            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Disposition", f"attachment; filename=\"middle_school_ebook_secret.pdf\"")
            self.send_header("Content-Length", str(os.path.getsize(pdf_path)))
            self.end_headers()
            with open(pdf_path, "rb") as f:
                self.wfile.write(f.read())
            return

        # 8. 온라인 리더기 (보안 토큰 인증)
        if path == "/view":
            token = query.get("token", [""])[0]
            order = verify_token(token)
            if not order:
                self.send_response(403)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("<h3>[접근 거부] 승인되지 않은 토큰입니다. 입금 확인 후 열람 가능합니다.</h3>".encode("utf-8"))
                return
            self.serve_file(os.path.join(BASE_DIR, "ebook_60p_expanded.html"), "text/html; charset=utf-8")
            return

        # 일반 파일 정적 서빙
        local_path = os.path.join(BASE_DIR, path.lstrip("/"))
        if os.path.exists(local_path) and os.path.isfile(local_path):
            mime_type, _ = mimetypes.guess_type(local_path)
            self.serve_file(local_path, mime_type or "application/octet-stream")
            return

        self.send_error(404, "Page Not Found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')
        
        try:
            data = json.loads(body) if body else {}
        except Exception:
            data = urllib.parse.parse_qs(body)
            data = {k: v[0] for k, v in data.items()}

        # 1. 구매자 주문 신청 접수
        if path == "/api/order":
            name = data.get("name", "").strip()
            email = data.get("email", "").strip()
            phone = data.get("phone", "").strip()
            if not name or not email:
                self.send_json(400, {"error": "성함과 이메일은 필수 입력 사항입니다."})
                return
            
            order_id, token = create_order(name, email, phone)
            self.send_json(200, {
                "success": True,
                "order_id": order_id,
                "buyer_name": name,
                "buyer_email": email,
                "price": 70000,
                "price_unit": "미소",
                "payment_method": "경제앱으로 박희망에게 입금",
                "message": "주문이 정상 접수되었습니다. 경제앱으로 박희망에게 70,000 미소를 입금해주시면 확인 즉시 이메일로 전자책 다운로드 링크가 자동 발송됩니다."
            })
            return

        # 2. 박희망 선생님 입금 확인 승인 & 즉시 이메일 자동 발송 트리거
        if path == "/api/approve":
            order_id = data.get("order_id", "").strip()
            if not order_id:
                self.send_json(400, {"error": "주문 ID가 누락되었습니다."})
                return
            
            order = approve_order(order_id)
            if not order:
                self.send_json(404, {"error": "해당 주문을 찾을 수 없습니다."})
                return
            
            # 메일 발송 실행!
            mail_result = send_ebook_email(
                buyer_name=order["buyer_name"],
                buyer_email=order["buyer_email"],
                access_token=order["access_token"],
                download_base_url="http://localhost:8000"
            )
            
            self.send_json(200, {
                "success": True,
                "order": order,
                "mail_result": mail_result,
                "message": f"{order['buyer_name']}님의 입금이 확인되어 {order['buyer_email']}로 전자책 다운로드 링크가 자동 전송되었습니다!"
            })
            return

        self.send_error(404, "Endpoint Not Found")

    def send_json(self, status, payload):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))

    def serve_file(self, filepath, mime_type):
        if not os.path.exists(filepath):
            self.send_error(404, "File Not Found")
            return
        self.send_response(200)
        self.send_header("Content-Type", mime_type)
        self.send_header("Content-Length", str(os.path.getsize(filepath)))
        self.end_headers()
        with open(filepath, "rb") as f:
            self.wfile.write(f.read())

    def serve_admin_dashboard(self):
        admin_html = """
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <title>6학년 3반 박희망 선생님 - 전자책 입금 관리 및 자동 발송 센터</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-slate-900 text-slate-100 min-h-screen p-8">
            <div class="max-w-5xl mx-auto">
                <div class="flex items-center justify-between pb-6 border-b border-slate-800">
                    <div>
                        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950 border border-cyan-800 text-cyan-400 text-xs font-semibold mb-2">
                            <span>●</span> 실시간 연동 서버 활성화
                        </div>
                        <h1 class="text-2xl font-bold">🏛️ 6학년 3반 박희망 선생님 입금 확인 & 전자책 자동 발송 센터</h1>
                        <p class="text-slate-400 text-sm mt-1">경제앱으로 70,000 미소 입금을 확인하신 후 <strong>[입금 확인 & 자동 발송]</strong> 버튼을 누르시면 구매자 메일로 즉시 전자책이 전송됩니다.</p>
                    </div>
                    <button onclick="fetchOrders()" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-sm font-semibold rounded-lg border border-slate-700">🔄 새로고침</button>
                </div>

                <div class="grid grid-cols-3 gap-4 my-6">
                    <div class="bg-slate-800/80 p-5 rounded-xl border border-slate-700">
                        <span class="text-xs text-slate-400">교재값 기준</span>
                        <div class="text-2xl font-black text-amber-400 mt-1">70,000 미소</div>
                    </div>
                    <div class="bg-slate-800/80 p-5 rounded-xl border border-slate-700">
                        <span class="text-xs text-slate-400">공식 결제 수단</span>
                        <div class="text-lg font-bold text-cyan-400 mt-1">경제앱으로 박희망에게 입금</div>
                    </div>
                    <div class="bg-slate-800/80 p-5 rounded-xl border border-slate-700">
                        <span class="text-xs text-slate-400">발송 대상 도서</span>
                        <div class="text-lg font-bold text-emerald-400 mt-1">44페이지 완결본 PDF</div>
                    </div>
                </div>

                <div class="bg-slate-800/60 rounded-xl border border-slate-700 overflow-hidden">
                    <div class="p-4 bg-slate-800 border-b border-slate-700 font-bold flex justify-between items-center">
                        <span>📋 실시간 주문 및 입금 승인 대기 목록</span>
                        <span id="order-count" class="text-xs font-normal text-slate-400">총 0건</span>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="w-full text-left text-sm">
                            <thead class="bg-slate-900/60 text-slate-400 text-xs uppercase border-b border-slate-700">
                                <tr>
                                    <th class="p-4">주문번호 / 일시</th>
                                    <th class="p-4">신청자 성함</th>
                                    <th class="p-4">수신 이메일</th>
                                    <th class="p-4">주문 금액</th>
                                    <th class="p-4">상태</th>
                                    <th class="p-4 text-center">원클릭 액션</th>
                                </tr>
                            </thead>
                            <tbody id="orders-tbody" class="divide-y divide-slate-700/50">
                                <tr>
                                    <td colspan="6" class="p-8 text-center text-slate-500">주문 내역을 불러오는 중...</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <script>
                async function fetchOrders() {
                    const res = await fetch('/api/orders');
                    const data = await res.json();
                    const tbody = document.getElementById('orders-tbody');
                    document.getElementById('order-count').innerText = `총 ${data.orders.length}건`;

                    if (data.orders.length === 0) {
                        tbody.innerHTML = `<tr><td colspan="6" class="p-8 text-center text-slate-500">아직 접수된 주문이 없습니다. 상세페이지에서 주문을 접수해보세요!</td></tr>`;
                        return;
                    }

                    tbody.innerHTML = data.orders.map(o => {
                        const isApproved = o.status === 'APPROVED';
                        const badge = isApproved 
                            ? `<span class="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-950 text-emerald-400 border border-emerald-800">✅ 발송 완료</span>`
                            : `<span class="px-2.5 py-1 rounded-full text-xs font-bold bg-amber-950 text-amber-400 border border-amber-800 animate-pulse">⏳ 입금 대기</span>`;

                        const actionBtn = isApproved
                            ? `<span class="text-xs text-slate-400">발송됨 (다운로드 ${o.download_count}회)</span>`
                            : `<button onclick="approveOrder('${o.order_id}')" class="px-3 py-1.5 bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs rounded-lg shadow-sm transition">⚡ 입금 확인 & 자동 발송</button>`;

                        return `
                            <tr class="hover:bg-slate-700/30">
                                <td class="p-4 font-mono text-xs text-slate-400">
                                    <div class="font-bold text-slate-200">${o.order_id}</div>
                                    <div class="text-[11px] text-slate-500">${o.created_at.slice(0, 19).replace('T', ' ')}</div>
                                </td>
                                <td class="p-4 font-bold text-white">${o.buyer_name}</td>
                                <td class="p-4 text-cyan-300 font-mono text-xs">${o.buyer_email}</td>
                                <td class="p-4 font-bold text-amber-400">${o.price.toLocaleString()} ${o.price_unit}</td>
                                <td class="p-4">${badge}</td>
                                <td class="p-4 text-center">${actionBtn}</td>
                            </tr>
                        `;
                    }).join('');
                }

                async function approveOrder(orderId) {
                    if (!confirm('경제앱으로 70,000 미소 입금을 확인하셨습니까?\n승인 시 즉시 구매자 이메일로 전자책 다운로드 링크가 자동 발송됩니다.')) return;
                    
                    const res = await fetch('/api/approve', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ order_id: orderId })
                    });
                    const data = await res.json();
                    if (data.success) {
                        alert(data.message);
                        fetchOrders();
                    } else {
                        alert('오류 발생: ' + (data.error || '승인 실패'));
                    }
                }

                fetchOrders();
            </script>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(admin_html.encode("utf-8"))

def run_server():
    from database import init_db, DB_PATH
    if not os.path.exists(DB_PATH):
        print("[AUTO_INIT] DB가 감지되지 않아 자동으로 초기화 및 원고 데이터를 적재합니다...")
        init_db()
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), EbookRequestHandler) as httpd:
        print(f"[SERVER_STARTED] 포트 {PORT} 에서 웹 서비스 및 API 가동 중...")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
