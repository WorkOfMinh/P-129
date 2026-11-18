# BRIEF â€” SC-04: SentinelIoT
*AI Agent PhÃ¡t Hiá»‡n Báº¥t ThÆ°á»ng Cáº£m Biáº¿n IoT (RÃ² Gas, ChÃ¡y, Ngáº­p NÆ°á»›c)*

---

### 1. Váº¥n Ä‘á»

Ban quáº£n lÃ½ (BQL) tÃ²a nhÃ  hiá»‡n nháº­n cáº£nh bÃ¡o tá»« cáº£m biáº¿n khÃ³i/gas/nhiá»‡t/nÆ°á»›c **rá»i ráº¡c theo tá»«ng Ä‘iá»ƒm**, khÃ´ng cÃ³ há»‡ thá»‘ng nÃ o phÃ¢n tÃ­ch tÆ°Æ¡ng quan giá»¯a chÃºng. Háº­u quáº£: khi 1 cáº£m biáº¿n lá»—i hoáº·c bÃ¡o trá»… nhÆ°ng cáº£m biáº¿n khÃ¡c á»Ÿ cÃ¹ng khu vá»±c Ä‘Ã£ cÃ³ tÃ­n hiá»‡u báº¥t thÆ°á»ng, BQL khÃ´ng biáº¿t Ä‘á»ƒ xá»­ lÃ½ sá»›m â€” nguy cÆ¡ bá» sÃ³t sá»± cá»‘ chÃ¡y/rÃ² gas giai Ä‘oáº¡n Ä‘áº§u. NgÆ°á»£c láº¡i, rule Ä‘Æ¡n láº» (vÃ­ dá»¥ cáº£m biáº¿n nháº¡y do bá»¥i/hÆ¡i nÆ°á»›c) gÃ¢y bÃ¡o Ä‘á»™ng nhiá»…u liÃªn tá»¥c, khiáº¿n Ä‘á»™i ká»¹ thuáº­t máº¥t tin tÆ°á»Ÿng vÃ  bá» qua cáº£nh bÃ¡o tháº­t.

### 2. NgÆ°á»i dÃ¹ng chÃ­nh

**Ká»¹ thuáº­t viÃªn Ban quáº£n lÃ½ tÃ²a nhÃ ** â€” ngÆ°á»i trá»±c tiáº¿p theo dÃµi há»‡ thá»‘ng cáº£m biáº¿n 24/7 vÃ  lÃ  ngÆ°á»i ra quyáº¿t Ä‘á»‹nh cuá»‘i cÃ¹ng (duyá»‡t/tá»« chá»‘i) vá»›i má»i lá»‡nh Ä‘iá»u khiá»ƒn thiáº¿t bá»‹ váº­t lÃ½.

### 3. Giáº£i phÃ¡p â€” luá»“ng chÃ­nh cá»§a Agent

1. **Thu tháº­p**: Agent nháº­n liÃªn tá»¥c dá»¯ liá»‡u tá»« 4 loáº¡i cáº£m biáº¿n (khÃ³i, gas, nhiá»‡t, ngáº­p nÆ°á»›c) qua MQTT.
2. **PhÃ¡t hiá»‡n**: So sÃ¡nh vá»›i baseline bÃ¬nh thÆ°á»ng cá»§a tá»«ng khu (Isolation Forest) + ngÆ°á»¡ng váº­t lÃ½ cá»©ng (rule-threshold).
3. **TÆ°Æ¡ng quan**: Náº¿u â‰¥ 2 cáº£m biáº¿n cÃ¹ng khu báº¥t thÆ°á»ng cÃ¹ng lÃºc (vÃ­ dá»¥ nhiá»‡t tÄƒng + khÃ³i tÄƒng), agent suy luáº­n nguy cÆ¡ cá»¥ thá»ƒ (LLM reasoning), kÃ¨m dá»¯ liá»‡u gá»‘c lÃ m cÄƒn cá»©.
4. **Äá» xuáº¥t & chá» duyá»‡t**: Hiá»ƒn thá»‹ cáº£nh bÃ¡o + hÃ nh Ä‘á»™ng Ä‘á» xuáº¥t (Ä‘Ã³ng van, kÃ­ch chuÃ´ng...) cho ká»¹ thuáº­t viÃªn; **chá» xÃ¡c nháº­n (HITL)** trÆ°á»›c khi thá»±c thi, trá»« ngÆ°á»¡ng nguy hiá»ƒm tÃ­nh máº¡ng Ä‘Ã£ Ä‘á»‹nh trÆ°á»›c thÃ¬ tá»± Ä‘á»™ng kÃ­ch hoáº¡t tá»‘i thiá»ƒu kÃ¨m log.
5. **Ghi log**: Má»i sá»± cá»‘, suy luáº­n, vÃ  quyáº¿t Ä‘á»‹nh (ká»ƒ cáº£ tá»« chá»‘i) Ä‘Æ°á»£c lÆ°u láº¡i Ä‘á»ƒ truy váº¿t sau nÃ y.

**SÆ¡ Ä‘á»“ minh há»a:**

```mermaid
flowchart TD
    A["1. Thu tháº­p<br/>MQTT: khÃ³i, gas, nhiá»‡t, nÆ°á»›c"] --> B["2. PhÃ¡t hiá»‡n<br/>Isolation Forest + ngÆ°á»¡ng cá»©ng"]
    B --> C["3. TÆ°Æ¡ng quan<br/>â‰¥2 cáº£m biáº¿n cÃ¹ng khu â†’ LLM suy luáº­n nguy cÆ¡"]
    C --> D["4. Äá» xuáº¥t & chá» duyá»‡t<br/>Hiá»ƒn thá»‹ cáº£nh bÃ¡o + Ä‘á» xuáº¥t hÃ nh Ä‘á»™ng"]
    D -->|NgÆ°á»¡ng nguy hiá»ƒm tÃ­nh máº¡ng| E["Tá»± Ä‘á»™ng kÃ­ch hoáº¡t tá»‘i thiá»ƒu<br/>(kÃ¨m log)"]
    D -->|TrÆ°á»ng há»£p cÃ²n láº¡i| F["Ká»¹ thuáº­t viÃªn xÃ¡c nháº­n<br/>Duyá»‡t / Tá»« chá»‘i (HITL)"]
    E --> G["5. Ghi log<br/>Má»i sá»± cá»‘, suy luáº­n & quyáº¿t Ä‘á»‹nh"]
    F --> G
```

### 4. Pháº¡m vi

**LÃ m:**
- Táº­p trung 2 ká»‹ch báº£n nguy hiá»ƒm chÃ­nh: **chÃ¡y** (nhiá»‡t + khÃ³i) vÃ  **rÃ² gas** (gas + nhiá»‡t).
- 4 loáº¡i cáº£m biáº¿n, dá»¯ liá»‡u **hoÃ n toÃ n giáº£ láº­p** qua MQTT simulator.
- Dashboard 2 vai trÃ² (CÆ° dÃ¢n xem / Ká»¹ thuáº­t BQL xá»­ lÃ½), HITL báº¯t buá»™c, log sá»± cá»‘.

**Chá»§ Ä‘á»™ng khÃ´ng lÃ m:**
- KhÃ´ng Ä‘iá»u khiá»ƒn thiáº¿t bá»‹ váº­t lÃ½ tháº­t â€” má»i lá»‡nh actuator cháº¡y trÃªn mÃ´i trÆ°á»ng mÃ´ phá»ng.
- KhÃ´ng lÃ m mÃ´ phá»ng lan truyá»n sá»± cá»‘ khÃ´ng gian hay gá»£i Ã½ lá»™ trÃ¬nh sÆ¡ tÃ¡n.
- KhÃ´ng dÃ¹ng LSTM, Digital Twin hay dá»¯ liá»‡u real-world (Building Data Genome, UK-DALE...) cho báº£n demo.

### 5. CÃ¡ch Ä‘o thÃ nh cÃ´ng

*Äo trÃªn bá»™ ká»‹ch báº£n mÃ´ phá»ng cá»§a nhÃ³m (cÃ³ inject anomaly cÃ³ kiá»ƒm soÃ¡t), khÃ´ng pháº£i dá»¯ liá»‡u production tháº­t â€” vÃ¬ sáº£n pháº©m cháº¡y 100% trÃªn mÃ´i trÆ°á»ng giáº£ láº­p trong 5 tuáº§n.*

| Chá»‰ sá»‘ | Má»¥c tiÃªu | CÃ¡ch Ä‘o |
|---|---|---|
| Tá»· lá»‡ báº¯t Ä‘Ãºng sá»± cá»‘ Ä‘Ã£ inject (recall) | â‰¥ 90% trÃªn ká»‹ch báº£n chÃ¡y + rÃ² gas | `classification_report` trÃªn táº­p test, cháº¡y â‰¥ 20 ká»‹ch báº£n/loáº¡i |
| BÃ¡o Ä‘á»™ng nháº§m (false positive) | â‰¤ 1 láº§n/ngÃ y mÃ´ phá»ng (24h dá»¯ liá»‡u baseline bÃ¬nh thÆ°á»ng) | Äáº¿m sá»‘ cáº£nh bÃ¡o Trung bÃ¬nh trá»Ÿ lÃªn khi khÃ´ng cÃ³ anomaly inject |
| Thá»i gian tá»« lÃºc anomaly xáº£y ra Ä‘áº¿n lÃºc cáº£nh bÃ¡o hiá»ƒn thá»‹ | â‰¤ 3 giÃ¢y (Ä‘o trung bÃ¬nh, mÃ´i trÆ°á»ng local/demo) | ChÃªnh lá»‡ch timestamp log, láº¥y trung bÃ¬nh trÃªn â‰¥ 20 láº§n |

### 6. PhÃ¢n cÃ´ng nhÃ³m (Ä‘á» xuáº¥t theo ká»¹ nÄƒng Ä‘Ã£ khai bÃ¡o â€” nhÃ³m Ä‘iá»u chá»‰nh láº¡i náº¿u cáº§n)

| ThÃ nh viÃªn | Máº£ng phá»¥ trÃ¡ch | CÄƒn cá»© |
|---|---|---|
| **HoÃ ng Minh** (TrÆ°á»Ÿng nhÃ³m) | Backend + Ä‘iá»u phá»‘i ká»¹ thuáº­t, LangGraph pipeline | Backend, Communication, Ä‘Ã£ há»c IoT (FPT Software x BÃ¡ch Khoa) |
| **Nguyá»…n Äá»©c Trá»ng** | Cáº£m biáº¿n & MQTT simulator, Anomaly Detection (Isolation Forest) | ChuyÃªn ngÃ nh Äiá»‡n tá»­ â€” phÃ¹ há»£p mÃ´ phá»ng Ä‘áº·c tÃ­nh cáº£m biáº¿n tháº­t |
| **VÅ© Quang DÅ©ng** | Data pipeline vÃ o DB + Prompt Engineering cho LLM correlation | Data Analysis, Data Engineering, Prompt Engineering |
| **Nguyá»…n Há»¯u Máº¡nh** | Frontend Dashboard (2 vai trÃ²) + UI/UX | Backend, UI/UX Design, Product/Project Management |

---
