# 📚 PROJECT MEMORY & KNOWLEDGE BASE (Agent 5: Archive)

## 1. 프로젝트 개요 및 최종 합의 사항
- **프로젝트명**: 예비 중1 공부 비법 전자책 《꿈을 여는 공부의 새벽》
- **지은이**: **6학년 3반 담임 선생님** (현장감과 공감대 극대화)
- **교재값 및 화폐 단위**: **7만 미소 (70,000 미소)** / 화폐 단위: **미소**
- **공식 결제 수단**: **경제앱으로 박희망에게 입금**
- **기지 및 작업 경로**: `G:\middle_school_ebook_project` (C 드라이브 접근 엄격 금지, G 드라이브 전용)
- **신청 폼 표준**: 불필요한 괄호 표기 일체 삭제 (`받으실 분 성함`, `연락처`)
- **타겟 정의**: 대한민국 초등학교 6학년 학생(실사용자) + 학부모(입금 지원자) 듀얼 구성
- **교재 분량 및 최종 배포 파일**: 
  - 원고: `ebook_manuscript.md`
  - 구매자 실물 열람/PDF 변환 뷰어: `G:\middle_school_ebook_project\ebook_60p_expanded.html (ebook_final.pdf)` (인쇄 시 완벽한 고해상도 출판용 PDF 생성)
  - 웹 상세페이지: `G:\middle_school_ebook_project\landing_page.html`
  - 표지 이미지: `G:\middle_school_ebook_project\cover.jpg` (나노바나나 양장본)

## 2. 군단 편제 및 최종 상태 (Final Legion Status)
| 요원 | 호출부호 | 담당 직무 | 최종 상태 | 주요 산출물 |
|---|---|---|---|---|
| **Agent 1** | **Prime** | 총괄 오케스트레이션 & 1,000만 미소 로드맵 | **Completed** | [PLAN_10M_EBOOK_LAUNCH.md](file:///G:/middle_school_ebook_project/PLAN_10M_EBOOK_LAUNCH.md) |
| **Agent 2** | **Iris** | 와디즈급 카드뉴스 상세페이지 & 비주얼 아트 | **Completed** | [landing_page.html](file:///G:/middle_school_ebook_project/landing_page.html), [cover.jpg](file:///G:/middle_school_ebook_project/cover.jpg) |
| **Agent 3** | **Cipher** | 유통 플랫폼 & 다이내믹 프라이싱 파이프라인 | **Completed** | [DISTRIBUTION_GUIDE.md](file:///G:/middle_school_ebook_project/DISTRIBUTION_GUIDE.md), [dynamic_pricing.py](file:///G:/middle_school_ebook_project/dynamic_pricing.py) |
| **Agent 4** | **Sentinel** | 법적 리스크(환불 규정) & 품질 무결점 감사 | **Completed** | [QA_AUDIT_REPORT.md](file:///G:/middle_school_ebook_project/QA_AUDIT_REPORT.md) |
| **Agent 5** | **Archive** | 지식 아카이빙 및 프로젝트 메모리 보존 | **Completed** | [PROJECT_MEMORY.md](file:///G:/middle_school_ebook_project/PROJECT_MEMORY.md) |
| **Agent 6** | **Oracle** | 10대 전 과목(국영수과사+역사/도덕/기가/정보/한문/음미체) 팩트체크 | **Completed** | [ebook_manuscript.md](file:///G:/middle_school_ebook_project/ebook_manuscript.md) |

## 3. 영구 보존 규약 (Conventions & Lessons Learned)
1. **중학교 10대 전 과목 커버리지 (대표님 피드백 반영)**:
   - 국·영·수 주요 과목만 공부한 학생들은 중학교 첫 시험에서 '도덕, 역사, 기가, 정보, 한문' 등의 복병 과목에서 C, D등급을 받아 전교 석차가 무너짐.
   - 2022 개정 필수 과목인 '정보(SW/AI)', '역사 3단 트리', '도덕 칸트vs공리주의', '기가 투상법 도면', '한문 부수 유추법', '예체능 태도 루브릭'까지 10대 전 과목을 총망라하여 60페이지 분량의 완전 무결한 전자책을 구축함.
2. **진짜 3페이지 인터랙티브 미리보기 리더 (대표님 피드백 반영)**:
   - "3페이지 미리보기"라고 해놓고 단순 2문단 요약으로 때우는 것은 독자 기만이며 전환율을 떨어뜨림.
   - [1P 표지&전체목차], [2P 프롤로그 전문], [3P 수행평가 공식]으로 구성된 실제 책 3페이지 분량의 탭/페이지네이션 전자책 뷰어를 구현하여 신뢰도와 구매 욕구를 극대화함.
3. **웹 렌더링 무결점 규칙 (LaTeX 잔재 박멸 - 대표님 피드백)**:
   - 마크다운 원고의 수식 기호(`$\rightarrow$`, `\times`)를 HTML에 그대로 넣으면 깨진 코드로 노출되어 신뢰도를 치명적으로 훼손함.
   - 반드시 브라우저 네이티브 유니코드 기호(`→`, `×`)로 완벽히 치환하여 웹 조판 완성도를 확보할 것.
1. **표지 디자인 트렌드 (대표님 피드백 반영 - 절대적 교훈)**:
   - 초등 6학년은 자신을 '어린이'가 아닌 '예비 중학생(청소년)'으로 인식함.
   - 유치한 아동용 만화 캐릭터는 6학년에게 '유치하다'는 반감을 사고, 학부모에게는 신뢰도를 떨어뜨림.
   - **나노바나나(Gemini 생성 엔진)**를 활용하여 《이토록 공부가 재미있어지는 순간》 등 국내 대형 서점 1위 베스트셀러의 품격(딥 네이비 양장본, 은은한 골드 타이포그래피, 새벽 창가 책상 일러스트)을 적용하여 신뢰도와 구매 전환율을 극대화함.
2. **디지털 콘텐츠 환불 고지 규정**:
   - 영상의 '3일 내 환불 가능' 오기재 실수를 교훈 삼아, 전자상거래법 제17조 제2항 제5호에 따른 '디지털 파일 발송 및 다운로드 링크 제공 후 환불 불가'를 모든 판매창에 명시함.
3. **소셜 미디어 알고리즘 해킹 규칙**:
   - 메타(스레드/인스타그램) 포스팅 시 본문에 외부 링크 삽입을 금지하고, 반드시 '첫 번째 댓글'에 구매 링크를 달아야 도달률을 보존할 수 있음.
3. **고민상담소 레버리지**:
   - 일방적 세일즈를 중단하고, 학부모들의 질문에 1:1로 실시간 맞춤 솔루션을 제공하는 것이 구매 전환율의 핵심 트리거임.



## 4. 데이터베이스 및 자동 이메일 발송 아키텍처 (최신 확장)
- **독립 데이터베이스**: G:\\middle_school_ebook_project\\ebook_system.db (SQLite3)
  - ook_meta: 도서 메타데이터 (제목, 저자, 70,000 미소, 경제앱으로 박희망에게 입금, 44페이지)
  - chapters: 10대 전 과목 43개 세부 섹션 본문 및 인덱스
  - orders: 주문 내역, 입금 상태(PENDING/APPROVED), 고유 다운로드 토큰, 다운로드 횟수
- **통합 백엔드 서버**: G:\\middle_school_ebook_project\\server.py (http://localhost:8000)
  - 관리자 대시보드 (/admin): 박희망 선생님 전용 원클릭 입금 확인 & 자동 발송 버튼
  - 외부 임베드 위젯 (/widget): 타 홈페이지에 1줄로 삽입 가능한 44P 표지+7만 미소 카드
  - 보안 다운로드 스트림 (/download?token=xxx): 승인된 토큰 보유자만 44P PDF 다운로드
- **자동 이메일 발송 엔진**: G:\\middle_school_ebook_project\\mailer.py
  - 입금 승인 즉시 구매자 이메일로 44페이지 PDF 다운로드 링크 자동 전송
  - mail_config.json을 통해 실제 SMTP(Gmail, Naver 등) 연동 또는 시뮬레이션 모드 지원
- **외부 연동 매뉴얼**: G:\\middle_school_ebook_project\\EXTERNAL_EMBED_GUIDE.md
