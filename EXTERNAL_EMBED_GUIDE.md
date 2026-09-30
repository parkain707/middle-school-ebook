# 🌐 [Cipher & Iris] 전자책 외부 홈페이지 연동 및 링크 배포 가이드

본 문서는 독립 데이터베이스(`ebook_system.db`)에 구축된 전자책 콘텐츠를 **외부의 다른 홈페이지, 블로그, 노션, 학급 홈페이지에 링크/위젯 형태로 손쉽게 게시**하고, **입금 확인 시 이메일로 자동 발송**되도록 운영하는 실전 연동 매뉴얼입니다.

---

## 1. 외부 홈페이지 게시용 3가지 코드 스니펫

### 📌 [방식 1] 가장 추천: 초경량 배너 카드 위젯 (Iframe)
다른 홈페이지의 원하는 위치에 아래 **단 1줄의 HTML 코드**를 붙여넣으면, 고해상도 양장본 표지 + 7만 미소 가격표 + [상세보기 / 신청하기] 팝업이 포함된 프리미엄 카드가 즉시 렌더링됩니다.

```html
<!-- 전자책 7만 미소 외부 배너 위젯 -->
<iframe src="http://내서버주소:8000/widget" width="100%" height="250" frameborder="0" style="border-radius: 16px; max-width: 480px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3);" scrolling="no"></iframe>
```

---

### 📌 [방식 2] 심플 버튼 & 텍스트 링크 (블로그 / 노션 / 게시판용)
HTML iframe 삽입이 불가능한 일반 텍스트 게시판이나 SNS, 알림장에는 아래 링크를 그대로 사용하십시오.

```html
<!-- 심플 텍스트 링크 -->
<p>
  <strong>📖 《꿈을 여는 공부의 새벽: 중학교 첫 시험 전교 1등 시크릿》</strong><br>
  - 지은이: 6학년 3반 담임 선생님 | 교재값: 70,000 미소<br>
  - 공식 결제: 경제앱으로 박희망에게 입금<br>
  👉 <a href="http://내서버주소:8000" target="_blank" style="color: #2563eb; font-weight: bold;">[전자책 3P 무료 미리보기 및 주문 신청하기]</a>
</p>
```

---

### 📌 [방식 3] 개발자용 JSON REST API 직접 연동
외부 홈페이지가 React, Vue, 또는 서버 사이드 웹사이트일 경우 메타데이터를 직접 호출할 수 있습니다.

- **엔드포인트**: `GET http://내서버주소:8000/api/meta`
- **반환 데이터 예시**:
```json
{
  "title": "꿈을 여는 공부의 새벽: 중학교 첫 시험 전교 1등 시크릿",
  "author": "6학년 3반 담임 선생님",
  "price": 70000,
  "price_unit": "미소",
  "payment_method": "경제앱으로 박희망에게 입금",
  "total_pages": 44,
  "publisher": "6학년 3반 교실 연구소"
}
```

---

## 2. 서버 구동 및 실시간 운영 흐름

### A. 서버 실행 (G 드라이브 내)
```bash
cd G:\middle_school_ebook_project
python server.py
```
> 서버가 가동되면 `http://localhost:8000`에서 모든 웹 서비스와 API가 활성화됩니다.

---

### B. 박희망 선생님의 입금 확인 & 원클릭 자동 발송 센터
- **관리자 페이지 URL**: `http://localhost:8000/admin`
- **운영 프로세스**:
  1. 구매자가 외부 홈페이지 위젯 또는 상세페이지에서 **이름**과 **이메일**을 입력하고 [주문 신청]을 완료합니다.
  2. 데이터베이스(`ebook_system.db`)의 `orders` 테이블에 상태가 **`⏳ 입금 대기 (PENDING)`**로 실시간 등록됩니다.
  3. 박희망 선생님이 학급 경제앱을 확인하여 **70,000 미소** 입금을 확인합니다.
  4. 관리자 페이지(`http://localhost:8000/admin`)에서 해당 주문의 **`[⚡ 입금 확인 & 자동 발송]`** 버튼을 1초 만에 클릭합니다.
  5. **발송 엔진(`mailer.py`)이 즉시 가동**되어 구매자의 이메일로 44페이지 완결본 PDF 다운로드 보안 링크가 자동 전송됩니다!

---

## 3. 실제 네이버 / Gmail SMTP 연동 방법 (선택 사항)
기본 설정은 `simulation_mode: true`로 되어 있어, 실제 메일 서버 연동 없이도 발송된 이메일 전문을 `G:\middle_school_ebook_project\sent_emails/` 폴더에 즉시 저장하여 확인할 수 있습니다.

실제 인터넷 이메일로 쏘고 싶으실 때는 `mail_config.json` 파일을 열어 아래와 같이 수정하시면 됩니다:
```json
{
  "simulation_mode": false,
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "smtp_user": "선생님계정@gmail.com",
  "smtp_password": "구글앱비밀번호16자리",
  "sender_name": "6학년 3반 담임 선생님 (박희망)",
  "sender_email": "선생님계정@gmail.com"
}
```
