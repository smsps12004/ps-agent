import streamlit as st
from anthropic import Anthropic
from datetime import datetime

client = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

ACCESS_CODES = {
    "BETA001": ("beta", "2026-05-19"),
    "BETA002": ("beta", "2026-05-19"),
    "BETA003": ("beta", "2026-05-19"),
    "SAILOR001": ("individual", "2026-05-12"),
    "SAILOR002": ("individual", "2026-05-12"),
    "SAILOR003": ("individual", "2026-05-12"),
    "SAILOR004": ("individual", "2026-05-12"),
    "SAILOR005": ("individual", "2026-05-12"),
    "PSSHOP001": ("shop", "2026-10-12"),
    "PSSHOP002": ("shop", "2026-10-12"),
    "PSSHOP003": ("shop", "2026-10-12"),
}

def check_access(code):
    code = code.strip().upper()
    if code not in ACCESS_CODES:
        return False, "invalid"
    _, expiry = ACCESS_CODES[code]
    if datetime.now() > datetime.strptime(expiry, "%Y-%m-%d"):
        return False, "expired"
    return True, ACCESS_CODES[code][0]

st.set_page_config(page_title="PS Agent", page_icon="⚓", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 50%, #1a0500 100%); }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0d1b2a 0%, #1a0500 100%); border-right: 2px solid #c9a84c; }
[data-testid="stSidebar"] p, [data-testid="stSidebar"] h1 { color: #c9a84c !important; }
h1 { color: #c9a84c !important; font-family: Georgia, serif !important; letter-spacing: 2px; }
[data-testid="stCaptionContainer"] p { color: #a0b4c8 !important; font-style: italic; }
[data-testid="stTabs"] button { color: #c9a84c !important; font-weight: bold; font-size: 16px; }
[data-testid="stTabs"] button[aria-selected="true"] { color: #ffffff !important; border-bottom: 2px solid #c9a84c !important; }
[data-testid="stButton"] button { background: linear-gradient(135deg, #8b0000, #c9a84c) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: bold !important; }
[data-testid="stChatInput"] { border: 1px solid #c9a84c !important; border-radius: 25px !important; }
[data-testid="stTextArea"] textarea { background: rgba(13,27,42,0.9) !important; border: 1px solid #c9a84c !important; color: white !important; border-radius: 8px !important; }
hr { border-color: #c9a84c !important; }
p, li { color: #d0d8e4 !important; }
h2, h3 { color: #c9a84c !important; }
strong { color: #c9a84c !important; }
</style>
""", unsafe_allow_html=True)

if "access_granted" not in st.session_state:
    st.session_state.access_granted = False
    st.session_state.access_type = None

if not st.session_state.access_granted:
    st.title("⚓ PS Agent")
    st.caption("by Strategic Sailor — Your AI Personnel Specialist")
    st.divider()
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("### 🔐 Enter Access Code")
        st.markdown("Contact Strategic Sailor to receive your access code.")
        code_input = st.text_input("Access Code", placeholder="Enter your code here", type="password")
        if st.button("Submit", type="primary"):
            valid, result = check_access(code_input)
            if valid:
                st.session_state.access_granted = True
                st.session_state.access_type = result
                st.rerun()
            elif result == "expired":
                st.error("This access code has expired. Contact Strategic Sailor to renew.")
            else:
                st.error("Invalid access code. Contact Strategic Sailor to get access.")
        st.markdown("---")
        st.caption("Contact: strategicsailor@gmail.com")
    st.stop()

access_label = {"beta": "Beta Tester", "individual": "Sailor", "shop": "PS Shop"}
st.title("⚓ PS Agent")
st.caption("by Strategic Sailor — Your AI Personnel Specialist")
st.divider()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["💬 Ask PS Agent", "📝 Draft a Document", "✍️ Eval Writer", "⚓ Reserve Command Mode", "📊 LES Decoder", "✈️ Travel Assistant"])

SYSTEM_PROMPT = """You are PS Agent, an expert U.S. Navy Personnel Specialist created by Strategic Sailor. Answer every question like a senior PS1 briefing a junior sailor or PS shop. Follow these rules for every response:

1. Always cite the applicable MILPERSMAN article number(s). If you use web search to find current guidance, cite the source.
2. Structure your answers with clear headers (e.g., **Overview**, **Requirements**, **Step-by-Step Process**, **Common Errors**, **References**).
3. Use numbered steps for any process or procedure.
4. Be thorough — do not cut answers short. A sailor or PS shop should be able to act on your answer without needing to look anything else up.
5. Flag any time-sensitive or frequently-updated policy (pay rates, advancement quotas, etc.) so the user knows to verify the latest figures.
6. End each answer with a **References** section listing the MILPERSMAN articles, instructions, or NAVADMINs cited."""

DRAFT_PROMPT = "You are PS Agent, an expert Navy PS. Draft official Navy personnel documents in proper military format. Use bracketed placeholders for missing info. List required enclosures at the end."

NSIPS_QUICK_ISSUES = [
    "Sailor not showing in NSIPS",
    "Drill points not updating",
    "Pay not processing",
    "Record won't open",
    "IDT not reflecting",
]

RESERVE_PS_PROMPT = """You are a senior Navy PS1 with 15 years of experience specializing in Selected Reserve (SELRES) administration at a Navy Operational Support Center (NOSC). You know RESPERSMAN, BUPERSINST 1001.39F, the JTR, DODFMR Volume 7A, NSIPS operations, and reserve pay systems inside and out. Answer questions like a seasoned NOSC PS1. Always cite the applicable instruction or regulation. Give numbered, actionable steps.

NSIPS DEEP KNOWLEDGE BASE:

1. NSIPS ACCESS & LOGIN: NSIPS requires CAC authentication. Supported browsers are Internet Explorer 11 and Microsoft Edge (IE compatibility mode) on NMCI. Non-NMCI users access via the NSIPS web portal with CAC. Common login issues: CAC certificates not updated (run CACUtility or contact help desk), browser not in compatibility mode, ActivClient not running, account locked after 3 failed attempts (supervisor must unlock via User Management). Roles are assigned by the NSIPS Security Manager at the command. Always verify your role permits the transaction needed before attempting.

2. PAGE 2 (DEPENDENCY RECORD) UPDATES: Navigate to Personnel > Record Maintenance > Dependency Application (NAVPERS 1070/602). Required documents: certified marriage certificate, birth certificates, adoption decrees as applicable. Changes sync to DEERS within 24-48 hours after approval. If DEERS doesn't update, verify the transaction shows "Approved" status in NSIPS — do not resubmit until confirming the first transaction failed. Common error: submitting duplicate dependency records causes a DEERS conflict that requires MNCC intervention.

3. IDT (DRILL) PROCESSING: Navigate to Pay > Reserve Pay > IDT Processing. Enter Unit Identification Code (UIC), drill date, MUTA count (MUTA-2, MUTA-4, etc.), and duty type (IDT, RUTA, ADT). Drill must be entered within 3 days of completion per RESPERSMAN 1001-020. RUTA (Readiness Management Period) requires prior authorization. Common errors: wrong MUTA count entered — requires correction via Pay Adjustment; drill date entered outside the pay period — system will reject; sailor not attached to unit in NSIPS — must process unit gain first.

4. PAY DISCREPANCY CORRECTIONS: Navigate to Pay > Adjustments > Pay Correction. Document the error with dates, amounts, and NSIPS transaction IDs. For IDT pay errors: submit DD Form 2131 (Claim for Reimbursement). For AT/ADT errors: verify orders are loaded in NSIPS under Orders Management before adjusting. RPAS (Reserve Pay and Allowance System) discrepancies require coordination with DFAS-Cleveland (1-888-332-7411). Always get a DFAS case number. Local fixes are limited to current and one prior pay period — anything older goes to MNCC.

5. SGLI ELECTIONS: Navigate to Personnel > Benefit Elections > SGLI. Sailor must complete SGLV 8286 (coverage election) and SGLV 8286A (beneficiary designation) — both must be on file. Coverage amounts: $0, $50K increments up to $500K maximum. Election changes take effect the 1st of the following month. Common error: beneficiary form submitted without coverage form (or vice versa) — NSIPS will show incomplete election. FSGLI (Family SGLI) for spouse is entered separately. If sailor declines coverage, declination must be witnessed and signed.

6. REENLISTMENTS IN NSIPS: Navigate to Personnel > Reenlistment/Extension > Reenlistment. Required fields: ceremony date, oath administrator name/rank, contract type, new EOS date. Supporting document: NAVPERS 1070/601 (Reenlistment/Extension Agreement). After entry, print the contract from NSIPS for wet signatures. Upload signed contract as an enclosure. EOS and SEAOS auto-update upon approval. If sailor has a bonus, load the bonus obligation separately under Bonuses before finalizing the reenlistment. Common error: reenlistment entered before bonus obligation — causes bonus pay failure.

7. EMERGENCY CONTACT UPDATES: Navigate to Personnel > Record Maintenance > Emergency Contact (EMED). This is separate from Page 2 dependents — EMED is for notification purposes only and does not affect entitlements or DEERS. Required fields: name, relationship, phone, address. No supporting documents required. Updates are immediate. Sailors should verify EMED at each drill weekend.

8. UNIT TRANSFERS: Losing unit processes detachment in NSIPS under Personnel > Transfers > Detachment. Gaining unit processes gain under Personnel > Transfers > Gain. Both transactions must be completed within 5 days of transfer date per RESPERSMAN. Transfer checklist includes: record review, SGLI verification, emergency contact update, Page 2 review, NEC verification, training record transfer. Common error: losing unit fails to detach — sailor appears in both units, causing duplicate pay. Escalate immediately to MNCC if duplicate pay occurs.

9. RATE/RANK CORRECTIONS: Navigate to Personnel > Advancements > Advancement Entry for legitimate advancements. For frocking: enter under Frocking with the frocking authorization document number. For erroneous entries: corrections require NAVPERS approval — submit via NSIPS Message Traffic to PERS-8. Do not attempt to reverse an advancement entry locally without MNCC authorization — this causes audit discrepancies. Common error: advancement entered with wrong DOR (Date of Rate) — DOR must match the NAVADMIN or advancement authorization.

10. NECs AND QUALIFICATIONS: Navigate to Personnel > Record Maintenance > NEC/Qualification. NEC additions require a source document: NEC school completion certificate, NAVPERS 1221/6, or applicable NAVADMIN. Warfare designators (ESWS, SW, AW, etc.) require completion certificate and CO authorization letter. NEC removal requires NAVPERS 1221/6 with CO signature. Common error: NEC entered without source document attached — will be rejected during record audit. Always upload supporting documents as enclosures.

11. SEPARATIONS IN NSIPS: Navigate to Personnel > Separations > Separation Processing. Required: DD-214 worksheet, separation authority (MILPERSMAN article), RE code authorization. Enter RELGDU (Release from Active Duty) date and separation type. System generates DD-214 draft — must be reviewed for accuracy before finalizing. Final pay coordination: notify DFAS 30 days prior. Common errors: wrong separation code entered (requires MNCC correction), SGLI not terminated before separation (causes post-separation billing), leave balance not zeroed out.

12. COMMON NSIPS ERROR CODES:
- ERR-001 (Record Locked): Another user has the record open — wait 15 min or contact NSIPS help desk to force unlock.
- ERR-014 (UIC Mismatch): Sailor's UIC in record doesn't match transaction UIC — verify correct unit attachment.
- ERR-022 (Date Out of Range): Transaction date falls outside valid processing window — verify pay period dates.
- ERR-031 (Duplicate Transaction): Same transaction already exists — check transaction history before resubmitting.
- ERR-045 (DEERS Sync Failure): Dependency change not syncing to DEERS — wait 48 hrs, then escalate to MNCC.
- ERR-067 (Role Insufficient): Your NSIPS role doesn't permit this transaction — contact your NSIPS Security Manager.
- ERR-089 (Contract Not Found): Reenlistment/extension contract not attached — upload signed contract before finalizing.

13. NSIPS TROUBLE TICKETS: Submit via the NSIPS Help Desk portal at nsipsprod.nmci.navy.mil (CAC required). Required information: UIC, sailor's EDIPI (last 4 SSN if EDIPI unavailable), transaction type, error message/code, steps already attempted, urgency (routine/priority/emergency). Expected response: routine 5-7 business days, priority 24-48 hours, emergency same day. Track tickets via the Help Desk portal using your ticket number. For emergencies affecting pay, call the NSIPS Help Desk directly: DSN 882-1781.

14. MNCC ESCALATION: Escalate to MNCC (1-833-330-6622 or askmncc.ahf.nmci.navy.mil) for: rate/rank corrections requiring NAVPERS approval, pay adjustments older than 2 pay periods, duplicate pay from transfer errors, DEERS sync failures unresolved after 5 business days, DD-214 corrections after separation, bonus discrepancies, IDES/MEB/PEB administrative actions. Have ready: sailor's EDIPI, UIC, specific error or issue description, NSIPS transaction IDs, and any prior correspondence with DFAS or help desk. Document every MNCC interaction with case number and representative name."""

with tab1:
    tab1_mode = st.radio("", ["💬 General PS Questions", "🖥️ NSIPS Troubleshooter"], horizontal=True, key="tab1_mode")
    st.divider()

    if tab1_mode == "💬 General PS Questions":
        if "messages" not in st.session_state:
            st.session_state.messages = []
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        if len(st.session_state.messages) == 0:
            st.markdown("**Common questions:**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Can a Sailor reenlist with a pending NJP?"):
                    st.session_state.starter = "Can a Sailor reenlist with a pending NJP?"
                if st.button("How do I process a hardship discharge?"):
                    st.session_state.starter = "How do I process a hardship discharge?"
            with col2:
                if st.button("What are the extension limits for an enlistment?"):
                    st.session_state.starter = "What are the extension limits for an enlistment?"
                if st.button("How do I correct an error on a DD-214?"):
                    st.session_state.starter = "How do I correct an error on a DD-214?"
        if "starter" in st.session_state and st.session_state.starter:
            prompt = st.session_state.starter
            st.session_state.starter = None
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Looking that up..."):
                    response = client.messages.create(
                        model="claude-opus-4-5", max_tokens=4096, system=SYSTEM_PROMPT,
                        tools=[{"type": "web_search_20250305", "name": "web_search"}],
                        messages=st.session_state.messages
                    )
                    answer = next((b.text for b in response.content if b.type == "text"), "")
                    st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()
        if prompt := st.chat_input("Ask any PS question..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Looking that up..."):
                    response = client.messages.create(
                        model="claude-opus-4-5", max_tokens=4096, system=SYSTEM_PROMPT,
                        tools=[{"type": "web_search_20250305", "name": "web_search"}],
                        messages=st.session_state.messages
                    )
                    answer = next((b.text for b in response.content if b.type == "text"), "")
                    st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()

    elif tab1_mode == "🖥️ NSIPS Troubleshooter":
        st.markdown("#### NSIPS Troubleshooter")
        st.caption("Describe your NSIPS issue and get step-by-step resolution guidance.")

        if "nsips_messages" not in st.session_state:
            st.session_state.nsips_messages = []

        for msg in st.session_state.nsips_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if len(st.session_state.nsips_messages) == 0:
            st.markdown("**Common NSIPS issues:**")
            cols = st.columns(3)
            for i, issue in enumerate(NSIPS_QUICK_ISSUES):
                with cols[i % 3]:
                    if st.button(issue, key=f"nsips_quick_{i}"):
                        st.session_state.nsips_starter = issue

        if "nsips_starter" in st.session_state and st.session_state.nsips_starter:
            prompt = st.session_state.nsips_starter
            st.session_state.nsips_starter = None
            st.session_state.nsips_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Looking that up..."):
                    response = client.messages.create(
                        model="claude-opus-4-5", max_tokens=4096,
                        system=RESERVE_PS_PROMPT,
                        tools=[{"type": "web_search_20250305", "name": "web_search"}],
                        messages=st.session_state.nsips_messages
                    )
                    answer = next((b.text for b in response.content if b.type == "text"), "")
                    st.markdown(answer)
            st.session_state.nsips_messages.append({"role": "assistant", "content": answer})
            st.rerun()

        if prompt := st.chat_input("Describe your NSIPS issue...", key="nsips_input"):
            st.session_state.nsips_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Looking that up..."):
                    response = client.messages.create(
                        model="claude-opus-4-5", max_tokens=4096,
                        system=RESERVE_PS_PROMPT,
                        tools=[{"type": "web_search_20250305", "name": "web_search"}],
                        messages=st.session_state.nsips_messages
                    )
                    answer = next((b.text for b in response.content if b.type == "text"), "")
                    st.markdown(answer)
            st.session_state.nsips_messages.append({"role": "assistant", "content": answer})
            st.rerun()

        if st.button("Clear NSIPS Chat", key="clear_nsips"):
            st.session_state.nsips_messages = []
            st.rerun()

with tab2:
    st.subheader("📝 Document Drafter")
    st.caption("Describe what you need and PS Agent will draft it.")
    doc_type = st.selectbox("Document Type", ["Hardship / Humanitarian Letter", "Reenlistment Request Letter", "Extension Request Letter", "Award Write-Up (NAM)", "Eval Bullets", "Page 13 Entry", "Request Chit", "Other"])
    sailor_info = st.text_area("Sailor Information & Details", placeholder="Example: PO2 Johnson, E-5, 6 years service, requesting hardship discharge to care for terminally ill mother in Chicago.", height=120)
    if st.button("Generate Document", type="primary"):
        if sailor_info.strip() == "":
            st.warning("Please enter sailor information first.")
        else:
            with st.spinner("Drafting document..."):
                response = client.messages.create(
                    model="claude-opus-4-5", max_tokens=4096, system=DRAFT_PROMPT,
                    tools=[{"type": "web_search_20250305", "name": "web_search"}],
                    messages=[{"role": "user", "content": f"Draft a {doc_type} with these details: {sailor_info}"}]
                )
                draft = next((b.text for b in response.content if b.type == "text"), "")
                st.divider()
                st.markdown("### Generated Document")
                st.markdown(draft)
                st.download_button(label="Download as Text File", data=draft, file_name="ps_agent_document.txt", mime="text/plain")

EVAL_SYSTEM_PROMPT = """You are a senior Navy Chief Petty Officer and expert eval writer with 20 years of experience writing and reviewing Navy performance evaluations (EVAL/FITREP). You know BUPERSINST 1610.10F and NAVPERS 1616/26 (E1-E6) inside and out.

Navy eval writing rules you always follow:
- Open every bullet with a strong past-tense action verb (LED, MANAGED, TRAINED, ACHIEVED, SPEARHEADED, ORCHESTRATED, MAINTAINED, EXCEEDED, etc.)
- Quantify everything possible (dollar amounts, percentages, personnel counts, time saved)
- Use standard Navy abbreviations (PO1, LCPO, CO, XO, PCS, NJP, NAM, ESWS, etc.)
- Write in active voice, no personal pronouns
- Bullets end with a semicolon; the final bullet in a block ends with a period
- Trait grades: 5.0=highest, 1.0=lowest; most marks fall 3.0-4.0; a 5.0 must be justified
- All output must be copy-paste ready for the actual NAVPERS 1616/26 form

NAVPERS 1616/26 BLOCK DEFINITIONS (BUPERSINST 1610.10F):
- Block 28 (COMMAND EMPLOYMENT/ACHIEVEMENTS): Brief prose describing the command's mission, operational employment, and any command-level awards during the period.
- Block 29 (PRIMARY/COLLATERAL/WATCHSTANDING DUTIES): One short abbreviated line. Format: PRIMARY DUTY/COLLATERAL DUTY/WATCHSTATION. Example: PS LPO/DEERS Op/SAPR VA.
- Block 33 (PROFESSIONAL KNOWLEDGE): Trait grade 1.0-5.0.
- Block 34 (QUALITY OF WORK): Trait grade 1.0-5.0.
- Block 35 (COMMAND OR ORGANIZATIONAL CLIMATE/EQUAL OPPORTUNITY): Trait grade 1.0-5.0.
- Block 36 (TEAMWORK): Trait grade 1.0-5.0.
- Block 37 (MILITARY BEARING/CHARACTER): Trait grade 1.0-5.0.
- Block 38 (LEADERSHIP): Trait grade 1.0-5.0.
- Block 39 (SUPERVISING/TRAINING): Trait grade 1.0-5.0.
- Block 40 (PROMOTION RECOMMENDATION): Valid marks: NOR / SP / Progressing / Promotable / Must Promote / Early Promote. Narrative justifying the mark, comparing to peers.
- Block 41 (RETENTION RECOMMENDATION): State whether Navy should retain, reenlist, or separate and why.
- Block 43 (COMMENTS ON PERFORMANCE): Main narrative. Bullet-formatted accomplishments and results. Each bullet ~100-120 characters. Up to ~16 lines.
- Block 44 (QUALIFICATIONS/ACHIEVEMENTS): Education, training, awards, community involvement. Bullet format.
"""

BLOCK_DESCRIPTIONS = {
    "Block 43 — Comments on Performance": "Main narrative. Bullet-formatted accomplishments, leadership, and quantified results. ~100-120 chars per bullet, up to ~16 lines.",
    "Block 44 — Qualifications / Achievements": "Education, training completed, awards received, community involvement, collateral duties. Bullet format.",
}

with tab3:
    st.subheader("✍️ Eval Writer")
    st.caption("Generate properly formatted Navy eval bullets and complete evaluations per NAVPERS 1616/26.")

    eval_tab_a, eval_tab_b = st.tabs(["🔹 Bullet Writer", "📄 Full Eval Generator"])

    # ── BULLET WRITER ──────────────────────────────────────────────────────────
    with eval_tab_a:
        st.markdown("#### Single Bullet Writer")
        st.caption("Describe what the sailor did in plain English. PS Agent will format it into a proper Navy eval bullet.")

        bullet_block = st.selectbox(
            "Block Type",
            list(BLOCK_DESCRIPTIONS.keys()),
            key="bullet_block"
        )
        st.caption(BLOCK_DESCRIPTIONS[bullet_block])

        bullet_input = st.text_area(
            "What did the sailor do?",
            placeholder="Example: She managed the division's training program and got everyone qualified ahead of schedule. She also mentored two junior sailors who both made E5.",
            height=130,
            key="bullet_input"
        )
        bullet_count = st.selectbox("How many bullets?", [1, 2, 3, 4, 5], key="bullet_count")

        if st.button("Generate Bullet(s)", type="primary", key="gen_bullets"):
            if not bullet_input.strip():
                st.warning("Describe what the sailor did first.")
            else:
                with st.spinner("Formatting bullets..."):
                    block_label = bullet_block.split("—")[0].strip()
                    block_desc = BLOCK_DESCRIPTIONS[bullet_block]
                    user_msg = (
                        f"Write exactly {bullet_count} Navy eval bullet(s) for {block_label} on the NAVPERS 1616/26 form.\n\n"
                        f"Block purpose: {block_desc}\n\n"
                        f"What the sailor did (plain English):\n{bullet_input}\n\n"
                        f"Rules:\n"
                        f"- Respect the character limit for this block\n"
                        f"- Format exactly as it would appear copy-pasted into the real form\n"
                        f"- Use bullet format with action verb openers\n"
                        f"- Return only the formatted text, ready to paste. No commentary."
                    )
                    response = client.messages.create(
                        model="claude-opus-4-5",
                        max_tokens=512,
                        system=EVAL_SYSTEM_PROMPT,
                        tools=[{"type": "web_search_20250305", "name": "web_search"}],
                        messages=[{"role": "user", "content": user_msg}]
                    )
                    bullets_out = next((b.text for b in response.content if b.type == "text"), "")
                    st.divider()
                    st.markdown("#### Generated Bullet(s)")
                    st.text_area("Copy from here:", value=bullets_out, height=160, key="bullets_result")

    # ── FULL EVAL GENERATOR ────────────────────────────────────────────────────
    with eval_tab_b:
        st.markdown("#### Full Eval Generator")
        st.caption("Fill in the sailor's info and performance details. PS Agent formats the complete NAVPERS 1616/26.")

        # ── Sailor Info
        col1, col2 = st.columns(2)
        with col1:
            eval_name    = st.text_input("Sailor Name", placeholder="Smith, John A.", key="eval_name")
            eval_rate    = st.text_input("Rate / Rank", placeholder="PS2 / E-5", key="eval_rate")
            eval_desig   = st.text_input("Designator / NEC", placeholder="2514", key="eval_desig")
        with col2:
            eval_command = st.text_input("Command", placeholder="USS EXAMPLE (DDG-99)", key="eval_command")
            eval_billet  = st.text_input("Billet / Position", placeholder="LPO, Personnel Department", key="eval_billet")
            eval_period  = st.text_input("Reporting Period", placeholder="20240101 – 20241231", key="eval_period")

        st.divider()

        # ── Block 28
        st.markdown("**Block 28 — Command Employment & Command Achievements** *(optional)*")
        st.caption("Describe the command's mission, deployment, major evolutions, and command-level awards this period.")
        b28_input = st.text_area(
            "Block 28",
            placeholder="USS EXAMPLE deployed to 5th Fleet AOR Aug-Feb, conducting FDNF operations and 47 at-sea days in support of OIF. Command awarded Battle E and CNO Safety Award.",
            height=85, key="b28", label_visibility="collapsed"
        )

        st.divider()

        # ── Block 29
        st.markdown("**Block 29 — Primary / Collateral / Watchstanding Duties**")
        st.caption("Short abbreviated line. Format: PRIMARY DUTY/COLLATERAL/WATCHSTATION")
        b29_input = st.text_input(
            "Block 29",
            placeholder="PS LPO/DEERS Operator/SAPR VA/CDO",
            key="b29", label_visibility="collapsed"
        )

        st.divider()

        # ── Blocks 33–39 Trait Grades
        st.markdown("**Blocks 33–39 — Performance Trait Grades**")
        st.caption("1.0–5.0 scale. Most grades fall 3.0–4.0. A 5.0 must be justified by documented exceptional performance.")
        tg1, tg2, tg3 = st.columns(3)
        with tg1:
            t33 = st.number_input("33 — Professional Knowledge",   min_value=1.0, max_value=5.0, value=4.0, step=0.2, key="t33")
            t36 = st.number_input("36 — Teamwork",                 min_value=1.0, max_value=5.0, value=4.0, step=0.2, key="t36")
        with tg2:
            t34 = st.number_input("34 — Quality of Work",          min_value=1.0, max_value=5.0, value=4.0, step=0.2, key="t34")
            t37 = st.number_input("37 — Military Bearing/Character",min_value=1.0, max_value=5.0, value=4.0, step=0.2, key="t37")
        with tg3:
            t35 = st.number_input("35 — Cmd/Org Climate / EO",     min_value=1.0, max_value=5.0, value=4.0, step=0.2, key="t35")
            t38 = st.number_input("38 — Leadership",               min_value=1.0, max_value=5.0, value=4.0, step=0.2, key="t38")
        t39 = st.number_input("39 — Supervising / Training",       min_value=1.0, max_value=5.0, value=4.0, step=0.2, key="t39")

        st.divider()

        # ── Block 40
        st.markdown("**Block 40 — Promotion Recommendation**")
        promo_rec = st.selectbox(
            "Promotion Mark",
            ["Early Promote", "Must Promote", "Promotable", "Progressing", "SP", "NOR"],
            key="promo_rec"
        )
        b40_input = st.text_area(
            "Narrative supporting the promotion mark",
            placeholder="Top performer among 14 PS2s at command. Performs at the E6 level daily. Should be advanced at first opportunity.",
            height=85, key="b40"
        )

        st.divider()

        # ── Block 41
        st.markdown("**Block 41 — Retention Recommendation**")
        retain_rec = st.selectbox(
            "Retention Mark",
            ["Retain", "Retain (Reenlist/Extend)", "Separate", "Retire"],
            key="retain_rec"
        )
        b41_input = st.text_area(
            "Narrative supporting retention recommendation",
            placeholder="Navy should reenlist this sailor. High performer with long-term career potential.",
            height=75, key="b41"
        )

        st.divider()

        # ── Blocks 43 & 44
        st.markdown("**Block 43 — Comments on Performance**")
        st.caption("Plain English — PS Agent formats into proper Navy eval bullets (~100-120 chars each, up to ~16 lines).")
        b43_input = st.text_area(
            "Block 43",
            placeholder="Led division through INSURV inspection, processed 450+ transactions with zero errors, managed $1.2M travel budget, mentored 4 junior sailors who all advanced...",
            height=140, key="b43", label_visibility="collapsed"
        )

        st.markdown("**Block 44 — Qualifications / Achievements**")
        st.caption("Education, training, awards, community involvement.")
        b44_input = st.text_area(
            "Block 44",
            placeholder="Completed AAS degree, received NAM, earned ESWS pin, volunteered 40 hrs community service, completed DL-1 leadership course...",
            height=100, key="b44", label_visibility="collapsed"
        )

        st.divider()

        if st.button("Generate Full Eval", type="primary", key="gen_full_eval"):
            required = [eval_name, eval_rate, eval_command, b29_input, b40_input, b41_input, b43_input, b44_input]
            if any(f.strip() == "" for f in required):
                st.warning("Please fill in: Sailor Name, Rate, Command, Block 29, Block 40, Block 41, Block 43, and Block 44.")
            else:
                with st.spinner("Writing evaluation..."):
                    full_eval_prompt = f"""Write a complete, copy-paste ready Navy performance evaluation for NAVPERS 1616/26 (E1-E6) per BUPERSINST 1610.10F.

SAILOR INFO:
- Name: {eval_name}
- Rate/Rank: {eval_rate}
- Designator/NEC: {eval_desig}
- Command: {eval_command}
- Billet/Position: {eval_billet}
- Reporting Period: {eval_period}

INPUTS — rewrite each into proper Navy eval format and label clearly (e.g. "BLOCK 28:"):

Block 28 — Command Employment/Achievements: {b28_input if b28_input.strip() else "N/A — omit this block"}
Block 29 — Primary/Collateral/Watchstanding Duties: {b29_input}

Block 33 — Professional Knowledge:              {t33}
Block 34 — Quality of Work:                     {t34}
Block 35 — Cmd/Org Climate / Equal Opportunity: {t35}
Block 36 — Teamwork:                            {t36}
Block 37 — Military Bearing/Character:          {t37}
Block 38 — Leadership:                          {t38}
Block 39 — Supervising/Training:                {t39}

Block 40 — Promotion Recommendation: Mark = {promo_rec}. Narrative: {b40_input}
Block 41 — Retention Recommendation: Mark = {retain_rec}. Narrative: {b41_input}

Block 43 — Comments on Performance (plain English, rewrite as eval bullets): {b43_input}
Block 44 — Qualifications/Achievements (plain English, rewrite as eval bullets): {b44_input}

OUTPUT FORMAT:
- BLOCK 28: prose paragraph (omit if N/A)
- BLOCK 29: single abbreviated line
- BLOCKS 33-39: clean table with block number, trait name, and grade
- BLOCK 40: promotion mark on first line, then narrative paragraph comparing to peers
- BLOCK 41: retention mark on first line, then one to two sentence narrative
- BLOCK 43: formatted bullets, ~100-120 chars each, up to ~16 lines
- BLOCK 44: formatted bullets

End with a one-line SUMMARY STATEMENT suitable for the promotion recommendation summary box."""

                    response = client.messages.create(
                        model="claude-opus-4-5",
                        max_tokens=4096,
                        system=EVAL_SYSTEM_PROMPT,
                        tools=[{"type": "web_search_20250305", "name": "web_search"}],
                        messages=[{"role": "user", "content": full_eval_prompt}]
                    )
                    full_eval_out = next((b.text for b in response.content if b.type == "text"), "")
                    st.divider()
                    st.markdown("### Generated Evaluation")
                    st.markdown(full_eval_out)
                    st.download_button(
                        label="📥 Download Eval as Text File",
                        data=full_eval_out,
                        file_name=f"eval_{eval_name.replace(' ', '_').replace(',', '')}.txt",
                        mime="text/plain"
                    )

# ── RESERVE COMMAND MODE CONSTANTS ────────────────────────────────────────────

RESERVE_MED_PROMPT = """You are a Navy administrative officer advising a Commanding Officer on medical readiness administrative procedures. You provide administrative and procedural guidance only. You never discuss individual medical conditions, diagnoses, treatments, medications, or personal health information. Your guidance covers forms, timelines, notification requirements, CO responsibilities, and administrative processes as defined in MANMED, MILPERSMAN, BUPERSINST, and SECNAVINST. Always include: 'Administrative guidance only — for individual medical questions, consult the Medical Officer or MTF.'"""

PAY_QUICK_ISSUES = [
    "IDT pay not received",
    "AT orders entitlements",
    "BAH eligibility for reservists",
    "RPAS pay discrepancy",
]

SELRES_DOC_TYPES = [
    "SELRES Reenlistment Package",
    "SELRES Extension Request",
    "Mobilization Orders Checklist",
    "Drill Weekend Muster Sheet",
    "NOSC Transfer Request",
]

CO_DECK_DOC_TYPES = [
    "NJP Paperwork",
    "Page 13 Entry",
    "Counseling Statement",
    "Letter of Caution (LOC)",
    "Letter of Instruction (LOI)",
    "Letter of Reprimand (LORAN)",
    "Separation Package",
    "Award Recommendation",
]

MOB_DOC_TYPES = [
    "Activation Orders Checklist",
    "Deployment Admin Package",
    "Pre-Deployment Checklist",
    "NOSC Readiness Report",
    "Post-Deployment Admin Checklist",
]

MED_ADMIN_TOPICS = [
    "How to read a medical readiness report",
    "PHA tracking and follow-up procedures",
    "Deployment medical clearance checklist",
    "LIMDU admin process (forms, timelines, notifications)",
    "Pregnancy notification admin — CO responsibilities",
    "Separation physical admin — PS shop requirements",
    "PDHA/PDHRA processing procedures",
    "Medical board referral — CO's role in MEB/PEB",
    "Immunization compliance tracking (admin only)",
    "How to request a medical readiness brief from Medical Officer",
]

RESERVE_SECTIONS = [
    "1 — SELRES Admin",
    "2 — CO Deck Work",
    "3 — Pay & Entitlements",
    "4 — Mobilization & Readiness",
    "5 — Medical Readiness (NOSC)",
    "6 — Command Health Dashboard",
]

# ── RESERVE COMMAND MODE TAB ───────────────────────────────────────────────────
with tab4:
    st.subheader("⚓ Reserve Command Mode")
    st.caption("Administrative tools for NOSC Commanding Officers and Reserve PS shops.")

    reserve_section = st.selectbox("Select Section", RESERVE_SECTIONS, key="reserve_section")

    st.divider()

    # ── SECTION 1: SELRES ADMIN ────────────────────────────────────────────────
    if reserve_section == RESERVE_SECTIONS[0]:
        st.markdown("#### SELRES Admin — Document Drafter")
        st.caption("Generate Selected Reserve administrative documents in proper military format.")

        selres_doc = st.selectbox("Document Type", SELRES_DOC_TYPES, key="selres_doc")
        selres_info = st.text_area(
            "Sailor / Unit Information & Details",
            placeholder="Example: IS2 Torres, E-5, 8 years SELRES, requesting reenlistment for 6 years. Current enlistment expires 15 Sep 2025. Assigned to NR NIOC Norfolk.",
            height=120, key="selres_info"
        )

        if st.button("Generate Document", type="primary", key="gen_selres"):
            if not selres_info.strip():
                st.warning("Enter sailor or unit information first.")
            else:
                with st.spinner("Drafting document..."):
                    response = client.messages.create(
                        model="claude-opus-4-5", max_tokens=4096,
                        system=RESERVE_PS_PROMPT,
                        tools=[{"type": "web_search_20250305", "name": "web_search"}],
                        messages=[{"role": "user", "content": f"Draft a {selres_doc} using the following information. Use proper military format. Use bracketed placeholders for any missing required information. List required enclosures at the end.\n\nDetails: {selres_info}"}]
                    )
                    doc_out = next((b.text for b in response.content if b.type == "text"), "")
                    st.divider()
                    st.markdown("### Generated Document")
                    st.markdown(doc_out)
                    st.download_button(
                        label="📥 Download as Text File",
                        data=doc_out,
                        file_name=f"SELRES_{selres_doc.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )

    # ── SECTION 2: CO DECK WORK ────────────────────────────────────────────────
    elif reserve_section == RESERVE_SECTIONS[1]:
        st.markdown("#### CO Deck Work — Document Drafter")
        st.caption("Generate Commanding Officer level administrative documents.")

        co_doc = st.selectbox("Document Type", CO_DECK_DOC_TYPES, key="co_doc")
        col_co1, col_co2 = st.columns(2)
        with col_co1:
            co_sailor = st.text_area(
                "Sailor Information",
                placeholder="Name, rate, paygrade, years of service, command, billet...",
                height=100, key="co_sailor"
            )
        with col_co2:
            co_situation = st.text_area(
                "Situation / Incident Details",
                placeholder="Describe what occurred, dates, witnesses, prior counseling, relevant facts...",
                height=100, key="co_situation"
            )

        if st.button("Generate Document", type="primary", key="gen_co_doc"):
            if not co_sailor.strip() or not co_situation.strip():
                st.warning("Enter both sailor information and situation details.")
            else:
                with st.spinner("Drafting document..."):
                    response = client.messages.create(
                        model="claude-opus-4-5", max_tokens=4096,
                        system=RESERVE_PS_PROMPT,
                        tools=[{"type": "web_search_20250305", "name": "web_search"}],
                        messages=[{"role": "user", "content": f"Draft a {co_doc} for a Commanding Officer. Use proper Navy military format. Use bracketed placeholders for any missing required information. List required enclosures at the end.\n\nSailor Information: {co_sailor}\n\nSituation/Details: {co_situation}"}]
                    )
                    co_out = next((b.text for b in response.content if b.type == "text"), "")
                    st.divider()
                    st.markdown("### Generated Document")
                    st.markdown(co_out)
                    st.download_button(
                        label="📥 Download as Text File",
                        data=co_out,
                        file_name=f"CO_{co_doc.replace(' ', '_').replace('/', '-')}.txt",
                        mime="text/plain"
                    )

    # ── SECTION 3: PAY & ENTITLEMENTS ─────────────────────────────────────────
    elif reserve_section == RESERVE_SECTIONS[2]:
        st.markdown("#### Pay & Entitlements")
        st.caption("Reserve pay questions answered by a senior PS1 specializing in SELRES pay and entitlements.")

        if "pay_messages" not in st.session_state:
            st.session_state.pay_messages = []

        for msg in st.session_state.pay_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if len(st.session_state.pay_messages) == 0:
            st.markdown("**Common pay issues:**")
            pay_cols = st.columns(2)
            for i, issue in enumerate(PAY_QUICK_ISSUES):
                with pay_cols[i % 2]:
                    if st.button(issue, key=f"pay_quick_{i}"):
                        st.session_state.pay_starter = issue

        if "pay_starter" in st.session_state and st.session_state.pay_starter:
            prompt = st.session_state.pay_starter
            st.session_state.pay_starter = None
            st.session_state.pay_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Looking that up..."):
                    response = client.messages.create(
                        model="claude-opus-4-5", max_tokens=4096,
                        system=RESERVE_PS_PROMPT,
                        tools=[{"type": "web_search_20250305", "name": "web_search"}],
                        messages=st.session_state.pay_messages
                    )
                    answer = next((b.text for b in response.content if b.type == "text"), "")
                    st.markdown(answer)
            st.session_state.pay_messages.append({"role": "assistant", "content": answer})
            st.rerun()

        if prompt := st.chat_input("Ask a reserve pay question...", key="pay_input"):
            st.session_state.pay_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Looking that up..."):
                    response = client.messages.create(
                        model="claude-opus-4-5", max_tokens=4096,
                        system=RESERVE_PS_PROMPT,
                        tools=[{"type": "web_search_20250305", "name": "web_search"}],
                        messages=st.session_state.pay_messages
                    )
                    answer = next((b.text for b in response.content if b.type == "text"), "")
                    st.markdown(answer)
            st.session_state.pay_messages.append({"role": "assistant", "content": answer})
            st.rerun()

        if st.button("Clear Pay Chat", key="clear_pay"):
            st.session_state.pay_messages = []
            st.rerun()

    # ── SECTION 4: MOBILIZATION & READINESS ───────────────────────────────────
    elif reserve_section == RESERVE_SECTIONS[3]:
        st.markdown("#### Mobilization & Readiness — Document Drafter")
        st.caption("Generate mobilization and readiness administrative documents and checklists.")

        mob_doc = st.selectbox("Document Type", MOB_DOC_TYPES, key="mob_doc")
        mob_info = st.text_area(
            "Unit / Sailor Information & Details",
            placeholder="Example: NR NIOC Norfolk, 45 assigned billets, 38 personnel, mobilizing 12 sailors to 5th Fleet AOR, departure date 15 Mar 2025...",
            height=120, key="mob_info"
        )

        if st.button("Generate Document", type="primary", key="gen_mob"):
            if not mob_info.strip():
                st.warning("Enter unit or sailor information first.")
            else:
                with st.spinner("Drafting document..."):
                    response = client.messages.create(
                        model="claude-opus-4-5", max_tokens=4096,
                        system=RESERVE_PS_PROMPT,
                        tools=[{"type": "web_search_20250305", "name": "web_search"}],
                        messages=[{"role": "user", "content": f"Draft a {mob_doc} for a Navy Reserve unit. Use proper military format. Use bracketed placeholders for any missing required information. Include all required checklist items per current RESPERSMAN guidance.\n\nDetails: {mob_info}"}]
                    )
                    mob_out = next((b.text for b in response.content if b.type == "text"), "")
                    st.divider()
                    st.markdown("### Generated Document")
                    st.markdown(mob_out)
                    st.download_button(
                        label="📥 Download as Text File",
                        data=mob_out,
                        file_name=f"MOB_{mob_doc.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )

    # ── SECTION 5: MEDICAL READINESS (NOSC) ───────────────────────────────────
    elif reserve_section == RESERVE_SECTIONS[4]:
        st.markdown("#### Medical Readiness (NOSC)")
        st.caption("Administrative and procedural guidance for COs and PS shops. No individual medical information.")
        st.info("⚠️ **Administrative guidance only.** This section covers forms, timelines, notifications, and CO responsibilities. For individual medical questions, consult your Medical Officer or MTF.", icon="⚠️")

        med_topic = st.selectbox("Select Topic", MED_ADMIN_TOPICS, key="med_topic")

        if st.button("Get Administrative Guidance", type="primary", key="gen_med"):
            with st.spinner("Retrieving guidance..."):
                response = client.messages.create(
                    model="claude-opus-4-5", max_tokens=4096,
                    system=RESERVE_MED_PROMPT,
                    tools=[{"type": "web_search_20250305", "name": "web_search"}],
                    messages=[{"role": "user", "content": f"Provide complete administrative guidance for a NOSC Commanding Officer and PS shop on the following topic: {med_topic}\n\nInclude: applicable instructions/references, required forms, timelines, step-by-step procedures, CO responsibilities, and any common administrative errors to avoid. Administrative and procedural guidance only — no individual medical information."}]
                )
                med_out = next((b.text for b in response.content if b.type == "text"), "")
                st.divider()
                st.markdown(f"### {med_topic}")
                st.markdown(med_out)
                st.markdown("---")
                st.caption("⚠️ Administrative guidance only. For individual medical questions, consult your Medical Officer or MTF.")
                st.download_button(
                    label="📥 Download Guidance",
                    data=med_out,
                    file_name=f"MedAdmin_{med_topic[:40].replace(' ', '_')}.txt",
                    mime="text/plain"
                )

    # ── SECTION 6: COMMAND HEALTH DASHBOARD ───────────────────────────────────
    elif reserve_section == RESERVE_SECTIONS[5]:
        st.markdown("#### Command Health Dashboard")
        st.caption("Input current readiness metrics to generate a Command Readiness Report.")

        st.markdown("**Enter current readiness percentage per category (0–100%):**")
        dash_col1, dash_col2 = st.columns(2)
        with dash_col1:
            r_personnel   = st.number_input("Personnel Readiness %",   min_value=0, max_value=100, value=80, step=1, key="r_personnel")
            r_medical     = st.number_input("Medical Readiness %",     min_value=0, max_value=100, value=75, step=1, key="r_medical")
            r_pay         = st.number_input("Pay Accuracy %",          min_value=0, max_value=100, value=90, step=1, key="r_pay")
        with dash_col2:
            r_mob         = st.number_input("Mobilization Readiness %",min_value=0, max_value=100, value=70, step=1, key="r_mob")
            r_training    = st.number_input("Training Readiness %",    min_value=0, max_value=100, value=85, step=1, key="r_training")

        dash_notes = st.text_area(
            "Known Issues / Notes (optional)",
            placeholder="Example: 4 sailors pending PHA completion, NSIPS pay issue affecting 2 IDT members, 3 billets unfilled...",
            height=90, key="dash_notes"
        )

        if st.button("Generate Readiness Report", type="primary", key="gen_dashboard"):
            overall = round((r_personnel + r_medical + r_pay + r_mob + r_training) / 5, 1)

            def status(pct):
                if pct >= 85: return "🟢 GREEN"
                elif pct >= 70: return "🟡 AMBER"
                else: return "🔴 RED"

            st.divider()
            st.markdown("### Command Readiness Overview")
            m1, m2, m3, m4, m5, m6 = st.columns(6)
            m1.metric("Overall", f"{overall}%")
            m2.metric("Personnel", f"{r_personnel}%")
            m3.metric("Medical", f"{r_medical}%")
            m4.metric("Pay", f"{r_pay}%")
            m5.metric("Mobilization", f"{r_mob}%")
            m6.metric("Training", f"{r_training}%")

            with st.spinner("Generating report..."):
                dash_prompt = f"""You are a senior Navy Reserve administrative officer generating a Command Readiness Report for a NOSC Commanding Officer.

READINESS METRICS:
- Personnel Readiness:    {r_personnel}% — {status(r_personnel)}
- Medical Readiness:      {r_medical}% — {status(r_medical)}
- Pay Accuracy:           {r_pay}% — {status(r_pay)}
- Mobilization Readiness: {r_mob}% — {status(r_mob)}
- Training Readiness:     {r_training}% — {status(r_training)}
- Overall Score:          {overall}%
- Color Status:           {status(overall)}

Known Issues/Notes: {dash_notes if dash_notes.strip() else "None provided"}

Generate a Command Readiness Report with the following sections:
1. EXECUTIVE SUMMARY — two sentences, overall status and trend
2. CATEGORY STATUS TABLE — block number, category, percentage, Green/Amber/Red
3. TOP 3 DEFICIENCIES — list only categories below 85%, ranked by severity
4. RECOMMENDED CORRECTIVE ACTIONS — one to three specific actions per deficiency, cite applicable instructions
5. 30/60/90 DAY ACTION PLAN — specific, measurable tasks with responsible party (CO, XO, LPO, PS shop)
6. COMMANDING OFFICER CERTIFICATION LINE — signature block placeholder

Write in official Navy report format. Be direct and actionable. No filler."""

                response = client.messages.create(
                    model="claude-opus-4-5", max_tokens=4096,
                    system=RESERVE_PS_PROMPT,
                    tools=[{"type": "web_search_20250305", "name": "web_search"}],
                    messages=[{"role": "user", "content": dash_prompt}]
                )
                report_out = next((b.text for b in response.content if b.type == "text"), "")
                st.markdown("### Command Readiness Report")
                st.markdown(report_out)
                st.download_button(
                    label="📥 Download Readiness Report",
                    data=report_out,
                    file_name="Command_Readiness_Report.txt",
                    mime="text/plain"
                )

# ── LES DECODER CONSTANTS ──────────────────────────────────────────────────────

LES_SYSTEM_PROMPT = """You are a senior Navy PS1 with 15 years of experience explaining Leave and Earnings Statements (LES) to junior sailors. You know DODFMR Volume 7A, the Joint Travel Regulation, and DFAS LES formatting inside and out.

Your job is to explain every field on the sailor's LES in plain English — like you're sitting across the desk from an E-3 who has never seen an LES before. Be clear, friendly, and thorough. Organize your explanation by section: Pay, Deductions, Entitlements, Leave, Tax Info, Retirement, and TSP.

For each field:
- State the field name
- Explain what it means in plain English
- State what the current value means for this sailor
- Flag anything that looks unusual, incorrect, or worth verifying with a ⚠️ warning

Common things to flag:
- BAH at wrong rate or dependency status
- SGLI coverage that seems inconsistent with sailor's stated wishes
- State tax being withheld for the wrong state
- YTD figures that don't match expected totals
- Leave balance below 0 or unusually high
- TSP contributions not set when sailor is eligible
- Missing entitlements the sailor may qualify for
- BRS vs legacy retirement discrepancies based on DIEMS date

Always end with: "This is an explanation tool only. Contact your PS shop for any corrections to your pay record."

Never recommend specific dollar amounts or tell the sailor what their pay should be — only explain what the LES shows and flag anomalies for follow-up."""

# ── LES DECODER TAB ────────────────────────────────────────────────────────────
with tab5:
    st.subheader("📊 LES Decoder")
    st.caption("Upload your Leave and Earnings Statement and PS Agent will explain every field in plain English.")
    st.info("🔒 Your LES contains sensitive information. This tool processes your document to explain it — no data is stored.", icon="🔒")

    les_input_method = st.radio(
        "How would you like to enter your LES?",
        ["📎 Upload PDF or Image", "✏️ Manual Entry"],
        horizontal=True,
        key="les_input_method"
    )

    les_text = ""

    # ── UPLOAD PATH ────────────────────────────────────────────────────────────
    if les_input_method == "📎 Upload PDF or Image":
        les_file = st.file_uploader(
            "Upload your LES (PDF, PNG, JPG, JPEG)",
            type=["pdf", "png", "jpg", "jpeg"],
            key="les_file"
        )

        if les_file is not None:
            import tempfile, os as _os

            try:
                import fitz
                pdf_available = True
            except ImportError:
                pdf_available = False

            try:
                import pytesseract
                from PIL import Image
                ocr_available = True
            except ImportError:
                ocr_available = False

            suffix = _os.path.splitext(les_file.name)[1].lower()
            with st.spinner("Reading your LES..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(les_file.read())
                    tmp_path = tmp.name
                try:
                    if suffix == ".pdf":
                        if not pdf_available:
                            st.error("PyMuPDF not installed. Run: pip install pymupdf — or use Manual Entry below.")
                        else:
                            doc = fitz.open(tmp_path)
                            les_text = "".join(page.get_text() for page in doc)
                    else:
                        if not ocr_available:
                            st.error("pytesseract/Pillow not installed. Run: pip install pytesseract pillow — or use Manual Entry below.")
                        else:
                            les_text = pytesseract.image_to_string(Image.open(tmp_path))
                finally:
                    _os.unlink(tmp_path)

            if les_text.strip():
                st.success("✅ LES text extracted. Review raw text below, then click Decode.")
                with st.expander("🔍 Show raw extracted text (for debugging)"):
                    st.text(les_text[:3000])
            else:
                st.warning("Could not extract text from this file. Try a clearer scan or switch to Manual Entry.")

    # ── MANUAL ENTRY PATH ──────────────────────────────────────────────────────
    else:
        st.markdown("Enter the values from your LES. Fill in what you have — leave blank fields empty.")

        with st.expander("💰 Pay", expanded=True):
            mc1, mc2 = st.columns(2)
            with mc1:
                m_base    = st.text_input("Base Pay ($)", key="m_base", placeholder="e.g. 2,467.80")
                m_specpay = st.text_input("Special Pay ($)", key="m_specpay", placeholder="e.g. 150.00")
                m_incpay  = st.text_input("Incentive Pay ($)", key="m_incpay", placeholder="e.g. 0.00")
            with mc2:
                m_bonus   = st.text_input("Bonus Pay ($)", key="m_bonus", placeholder="e.g. 0.00")
                m_gross   = st.text_input("Gross Pay ($)", key="m_gross", placeholder="e.g. 2,617.80")
                m_net     = st.text_input("Net Pay ($)", key="m_net", placeholder="e.g. 1,984.22")

        with st.expander("➖ Deductions"):
            md1, md2 = st.columns(2)
            with md1:
                m_fedtax  = st.text_input("Federal Tax ($)", key="m_fedtax")
                m_sttax   = st.text_input("State Tax ($) & State", key="m_sttax", placeholder="e.g. 45.00 VA")
                m_fica    = st.text_input("FICA / Social Security ($)", key="m_fica")
                m_medi    = st.text_input("Medicare ($)", key="m_medi")
            with md2:
                m_sgli    = st.text_input("SGLI ($) & Coverage Amount", key="m_sgli", placeholder="e.g. 25.00 / $400K")
                m_mgib    = st.text_input("MGIB ($)", key="m_mgib")
                m_afrh    = st.text_input("AFRH ($)", key="m_afrh")
                m_dental  = st.text_input("Dental ($)", key="m_dental")

        with st.expander("🏠 Entitlements"):
            me1, me2 = st.columns(2)
            with me1:
                m_bah     = st.text_input("BAH ($) & Dependency Status", key="m_bah", placeholder="e.g. 1,245.00 W/DEP")
                m_bas     = st.text_input("BAS ($)", key="m_bas")
            with me2:
                m_oha     = st.text_input("OHA ($)", key="m_oha")
                m_cola    = st.text_input("COLA ($)", key="m_cola")

        with st.expander("🏖️ Leave"):
            ml1, ml2 = st.columns(2)
            with ml1:
                m_lv_bf   = st.text_input("Leave Brought Forward", key="m_lv_bf")
                m_lv_acc  = st.text_input("Leave Accrued", key="m_lv_acc")
                m_lv_used = st.text_input("Leave Used", key="m_lv_used")
            with ml2:
                m_lv_cr   = st.text_input("Current Leave Balance", key="m_lv_cr")
                m_lv_proj = st.text_input("Projected End Balance", key="m_lv_proj")
                m_lv_lose = st.text_input("Use/Lose", key="m_lv_lose")

        with st.expander("🧾 Tax Info"):
            mt1, mt2 = st.columns(2)
            with mt1:
                m_fed_ms  = st.text_input("Fed Marital Status / Exemptions", key="m_fed_ms", placeholder="e.g. S/1")
                m_st_ms   = st.text_input("State Marital Status / Exemptions", key="m_st_ms")
                m_addl    = st.text_input("Additional Fed Withholding ($)", key="m_addl")
            with mt2:
                m_ytd_fed = st.text_input("YTD Federal Tax ($)", key="m_ytd_fed")
                m_ytd_st  = st.text_input("YTD State Tax ($)", key="m_ytd_st")
                m_ytd_fica= st.text_input("YTD FICA ($)", key="m_ytd_fica")

        with st.expander("🎖️ Retirement"):
            mr1, mr2 = st.columns(2)
            with mr1:
                m_ret_plan= st.text_input("Retirement Plan (RS / BRS / FERS)", key="m_ret_plan")
                m_diems   = st.text_input("DIEMS Date", key="m_diems", placeholder="e.g. 20180601")
            with mr2:
                m_ytd_ret = st.text_input("YTD Retirement Deduction ($)", key="m_ytd_ret")

        with st.expander("💼 TSP"):
            ms1, ms2 = st.columns(2)
            with ms1:
                m_tsp_pct = st.text_input("TSP Contribution %", key="m_tsp_pct")
                m_tsp_ytd = st.text_input("TSP YTD ($)", key="m_tsp_ytd")
            with ms2:
                m_tsp_roth= st.text_input("TSP Roth YTD ($)", key="m_tsp_roth")

        st.markdown("**Additional Fields**")
        af1, af2, af3 = st.columns(3)
        with af1:
            m_pay_date = st.text_input("Pay Date", key="m_pay_date", placeholder="e.g. 20250401")
            m_pebd     = st.text_input("PEBD", key="m_pebd", placeholder="e.g. 20180601")
        with af2:
            m_ets      = st.text_input("ETS Date", key="m_ets", placeholder="e.g. 20260601")
            m_paygrade = st.text_input("Pay Grade", key="m_paygrade", placeholder="e.g. E-4")
        with af3:
            m_ytd_gross= st.text_input("YTD Gross Pay ($)", key="m_ytd_gross")
            m_ytd_net  = st.text_input("YTD Net Pay ($)", key="m_ytd_net")

        les_text = f"""LES MANUAL ENTRY:
Pay Grade: {m_paygrade} | Pay Date: {m_pay_date} | PEBD: {m_pebd} | ETS: {m_ets}
BASE PAY: {m_base} | SPECIAL PAY: {m_specpay} | INCENTIVE PAY: {m_incpay} | BONUS: {m_bonus}
GROSS PAY: {m_gross} | NET PAY: {m_net} | YTD GROSS: {m_ytd_gross} | YTD NET: {m_ytd_net}
DEDUCTIONS — FED TAX: {m_fedtax} | STATE TAX: {m_sttax} | FICA: {m_fica} | MEDICARE: {m_medi}
SGLI: {m_sgli} | MGIB: {m_mgib} | AFRH: {m_afrh} | DENTAL: {m_dental}
ENTITLEMENTS — BAH: {m_bah} | BAS: {m_bas} | OHA: {m_oha} | COLA: {m_cola}
LEAVE — BF: {m_lv_bf} | ACCRUED: {m_lv_acc} | USED: {m_lv_used} | CURRENT: {m_lv_cr} | PROJECTED: {m_lv_proj} | USE/LOSE: {m_lv_lose}
TAX INFO — FED STATUS: {m_fed_ms} | STATE STATUS: {m_st_ms} | ADDL WITHHOLDING: {m_addl}
YTD — FED TAX: {m_ytd_fed} | STATE TAX: {m_ytd_st} | FICA: {m_ytd_fica}
RETIREMENT — PLAN: {m_ret_plan} | DIEMS: {m_diems} | YTD DEDUCTION: {m_ytd_ret}
TSP — CONTRIBUTION %: {m_tsp_pct} | YTD: {m_tsp_ytd} | ROTH YTD: {m_tsp_roth}"""

    # ── DECODE BUTTON & OUTPUT ─────────────────────────────────────────────────
    st.divider()
    if st.button("🔍 Decode My LES", type="primary", key="decode_les"):
        if not les_text.strip() or les_text.strip() == "LES MANUAL ENTRY:" + "\n" + "Pay Grade:  | Pay Date:  | PEBD:  | ETS: ":
            st.warning("Enter your LES data first — upload a file or fill in the manual entry fields.")
        else:
            with st.spinner("PS Agent is reading your LES..."):
                decode_prompt = f"""A sailor has provided their Leave and Earnings Statement. Explain every field present in plain English, organized by section: Pay, Deductions, Entitlements, Leave, Tax Info, Retirement, and TSP. For each field explain what it is and what the sailor's specific value means. Flag anything unusual with ⚠️. End your response with the disclaimer.

LES DATA:
{les_text}"""
                response = client.messages.create(
                    model="claude-opus-4-5",
                    max_tokens=4096,
                    system=LES_SYSTEM_PROMPT,
                    tools=[{"type": "web_search_20250305", "name": "web_search"}],
                    messages=[{"role": "user", "content": decode_prompt}]
                )
                explanation = next((b.text for b in response.content if b.type == "text"), "")
                st.session_state.les_explanation = explanation
                st.session_state.les_messages = [
                    {"role": "user", "content": decode_prompt},
                    {"role": "assistant", "content": explanation}
                ]

    if "les_explanation" in st.session_state and st.session_state.les_explanation:
        st.divider()
        st.markdown("### 📋 Your LES Explained")
        st.markdown(st.session_state.les_explanation)
        st.warning("⚠️ This is an explanation tool only. Contact your PS shop for any corrections to your pay record.")
        st.download_button(
            label="📥 Download LES Explanation",
            data=st.session_state.les_explanation,
            file_name="LES_Explanation.txt",
            mime="text/plain"
        )

        st.divider()
        st.markdown("#### 💬 Ask a Follow-Up Question About Your LES")
        st.caption("PS Agent has context from your LES explanation above.")

        for msg in st.session_state.les_messages[2:]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if followup := st.chat_input("Ask anything about your LES...", key="les_followup"):
            st.session_state.les_messages.append({"role": "user", "content": followup})
            with st.chat_message("user"):
                st.markdown(followup)
            with st.chat_message("assistant"):
                with st.spinner("Looking that up..."):
                    response = client.messages.create(
                        model="claude-opus-4-5",
                        max_tokens=4096,
                        system=LES_SYSTEM_PROMPT,
                        tools=[{"type": "web_search_20250305", "name": "web_search"}],
                        messages=st.session_state.les_messages
                    )
                    answer = next((b.text for b in response.content if b.type == "text"), "")
                    st.markdown(answer)
            st.session_state.les_messages.append({"role": "assistant", "content": answer})
            st.rerun()

        if st.button("Clear LES & Start Over", key="clear_les"):
            st.session_state.les_explanation = ""
            st.session_state.les_messages = []
            st.rerun()

# ── TRAVEL ASSISTANT CONSTANTS ─────────────────────────────────────────────────

TRAVEL_SYSTEM_PROMPT = """You are a senior Navy PS1 and certified Defense Travel Administrator with 15 years of experience processing travel claims, DTS vouchers, PCS orders, and reserve travel entitlements. You advise PS shops, travel clerks, and sailors on every aspect of Navy travel policy.

REGULATORY KNOWLEDGE:
- Joint Travel Regulation (JTR) — governing document for all DoD travel (replaced JFTR in 2015); travel.dod.mil
- DODFMR Volume 9 — travel pay and allowances
- NAVSUP Publication 200 — Navy supply travel procedures
- RESPERSMAN 1001 series — Reserve travel and pay
- MILPERSMAN 1300 series — PCS/orders policy
- GSA.gov — CONUS per diem rates (updated 1 Oct annually)
- PDTATAC — OCONUS per diem rates (updated monthly)
- DTS Policy at dtsproweb.defensetravel.osd.mil

ORDER TYPES AND ENTITLEMENTS:

PCS (Permanent Change of Station) — JTR Chapter 5 (Active Duty) / Chapter 10 (Reserve):
- Travel per diem en route to new PDS
- DLA (Dislocation Allowance) — offsets cost of moving household
- TLE (Temporary Lodging Expense) — up to 10 days CONUS, 60 days OCONUS
- MALT (Monetary Allowance in Lieu of Transportation) — POV mileage at published rate
- HHG/UB shipment — household goods and unaccompanied baggage
- TQSE/TQSA — temporary quarters subsistence expense
- Report-not-later-than (RNLTD) date governs travel window

TAD (Temporary Additional Duty) — JTR Chapter 2:
- Per diem at actual lodging cost + M&IE (or flat rate if gov quarters available)
- Rental car must be authorized in orders or by AO
- Government meals proportionally reduce M&IE
- Submit DD 1351-2 within 5 business days of return (JTR 2.1)

IDTT (Inactive Duty Training Travel) — JTR 10206 (Reserve-specific):
- Authorized when round-trip travel exceeds 50 miles or requires overnight stay
- Same per diem structure as TAD
- Orders must specifically state IDTT authorization
- Common error: claiming IDTT when 50-mile threshold not met — automatically disqualified

AT (Annual Training) — JTR Chapter 10 (Reserve):
- Travel from home of record (HOR) or PDS to training site — lesser of the two distances
- Per diem at 75% on travel days, full rate at training location
- Orders must show fund cite for travel
- Typically 2 weeks (14 days) maximum per fiscal year without special authorization

ADT (Active Duty for Training) — JTR Chapter 10 (Reserve):
- Same travel entitlements as AT; distinction is in the duty type code
- May include BAH and BAS if extended beyond IDT threshold

IDT (Inactive Duty Training) — JTR 1026:
- No travel entitlement for routine drill at assigned unit
- Travel only authorized when CO specifically directs it and orders reflect that authorization

DD FORM 1351-2 (TRAVEL VOUCHER OR SUBVOUCHER) — BLOCK BY BLOCK:
Block 1 — Payment: EFT direct deposit, split disbursement to GTC (mandatory when GTC used), or check
Block 2 — Name: Last, First, MI — must match DEERS/pay record exactly
Block 3 — Grade: Pay grade (E-5, O-3, etc.)
Block 4 — SSN: Full SSN on secure systems only; last 4 on unclassified copies
Block 5 — Taxpayer ID: Leave blank for military members
Block 6 — Period of Travel: From/To dates matching orders exactly
Block 7 — Organization: Unit name and UIC
Block 8 — Purpose of Travel: Reference orders number, type, and issuing authority
Block 9 — Itinerary: Each travel leg with date, city, mode of transport, per diem claimed
Block 10 — Reimbursable Expenses: All expenses >$75 itemized with receipts; lodging receipts required regardless of amount
Block 11 — Advance/Payments: DTS advances, GTC split disbursement amounts already paid
Block 12 — Accounting Classification: Fund cite from orders — must match exactly
Block 13 — Signature: Member signature and date
Block 14 — Approving Official: AO signature, date, title, phone

DD FORM 1351-6 (MULTI-PURPOSE CONTINUATION SHEET):
- Used when Block 9 itinerary or Block 10 expenses exceed space on DD 1351-2
- Must reference the parent DD 1351-2 date and traveler name at top
- All per diem calculations shown line by line
- Required enclosures listed at bottom

COMMON TRAVEL CLAIM ERRORS:
1. No lodging receipts — required for all commercial lodging, every night
2. M&IE not reduced for government-provided meals
3. POV mileage from wrong origin — must use lesser of: distance from home or from PDS
4. Missing orders as enclosure — mandatory with every voucher
5. IDTT claimed without meeting 50-mile round-trip threshold
6. Wrong per diem rate — always verify exact city/zip at GSA or PDTATAC
7. Rental car without written authorization in orders or from AO
8. GTC split disbursement omitted when GTC was used — mandatory per DTS policy
9. Voucher submitted more than 5 business days after return — late submission flag
10. Advance not reconciled — unreconciled advances create debt in MMPA

PER DIEM RATES (FY2025 REFERENCE):
Standard CONUS rate: $157 lodging + $68 M&IE = $225/day (non-listed locations)
High-cost areas (DC, NYC, SF, etc.): higher rates — verify at GSA.gov by zip code
M&IE breakdown: Breakfast 20%, Lunch 25%, Dinner 35%, Incidentals 20%
First/last travel day: 75% of M&IE only (no lodging if returning home same day)
Government meal deductions (FY2025 standard): Breakfast $13.60, Lunch $17.00, Dinner $37.40
OCONUS: Verify at PDTATAC — rates vary widely by country and city; updated monthly

DTS (DEFENSE TRAVEL SYSTEM):
Access: dtsproweb.defensetravel.osd.mil (CAC required)
Workflow: Create Authorization → Travel → Create Voucher → Submit to AO
Common errors: duplicate authorizations, wrong fund cite, AO not assigned, GTCC charges unmatched
Voucher amendments: use "Amend Voucher" — never create a duplicate voucher
Split disbursement: must match GTCC charges to the cent or DTS will reject
DTS Help Desk: 1-888-435-7146

NROWS (NAVY RESERVE ORDER WRITING SYSTEM):
Access: nrows.navy.mil (CAC required)
Order types: AT, ADT, ADSW, IDTT, MOB, IADT
Routing: NOSC Admin → Unit CO → Orders Issuing Authority → Fund Certifier
Common issues: fund cite not loaded, end strength ceiling exceeded, billet not coded for requested order type, orders not routed before travel date
Amendments: submit amendment request in NROWS; do not travel before amendment is approved
NROWS Help Desk: 1-800-621-8853

NSIPS/MMPA TRAVEL IMPACT:
- PCS gains/losses must be entered in NSIPS within 5 days of transfer (RESPERSMAN)
- Travel advances appear in MMPA as debts until voucher is approved and offset
- Unreconciled advances 90+ days old referred to DFAS-Cleveland for collection
- BAH changes effective date of PCS must match NSIPS transaction date
- DLA is processed through DFAS after NSIPS reflects PCS gain
- MMPA corrections for travel overpayments: submit DD 2131 to DFAS

Always cite the applicable JTR chapter and verify rates at GSA.gov (CONUS) or PDTATAC (OCONUS)."""

TRAVEL_SECTIONS = [
    "1 — Travel Claims",
    "2 — DTS Help",
    "3 — NROWS",
    "4 — Per Diem",
    "5 — NSIPS / MMPA",
    "6 — Ask Travel Agent",
]

TRAVEL_ORDER_TYPES = ["TAD", "PCS", "AT (Annual Training)", "ADT", "IDTT", "IDT (authorized travel)"]

TRAVEL_DTS_ISSUES = [
    "Voucher rejected by AO",
    "GTCC charges not matching",
    "Duplicate authorization created",
    "Fund cite error on authorization",
    "How to amend an approved voucher",
]

TRAVEL_NROWS_ISSUES = [
    "Orders not routing past NOSC Admin",
    "Fund cite not loading",
    "End strength ceiling exceeded",
    "How to request an amendment",
    "Billet not coded for order type",
]

TRAVEL_MMPA_ISSUES = [
    "Travel advance showing as debt",
    "Unreconciled advance 90+ days",
    "DLA not received after PCS",
    "BAH not updated after PCS",
    "DFAS debt letter received for travel",
]

# ── TRAVEL ASSISTANT TAB ────────────────────────────────────────────────────────
with tab6:
    st.subheader("✈️ Travel Assistant")
    st.caption("DD 1351-2, DTS, NROWS, Per Diem, NSIPS/MMPA — Active Duty and Reserve travel guidance.")

    travel_section = st.selectbox("Select Section", TRAVEL_SECTIONS, key="travel_section")
    st.divider()

    # ── SECTION 1: TRAVEL CLAIMS ───────────────────────────────────────────────
    if travel_section == TRAVEL_SECTIONS[0]:
        st.markdown("#### Travel Claims — DD 1351-2 / DD 1351-6 Drafter")
        st.caption("Enter your travel details and PS Agent will walk through every block, flag errors, and draft your claim.")

        tc_col1, tc_col2 = st.columns(2)
        with tc_col1:
            tc_order_type = st.selectbox("Order Type", TRAVEL_ORDER_TYPES, key="tc_order_type")
            tc_name       = st.text_input("Sailor Name (Last, First MI)", placeholder="Smith, John A.", key="tc_name")
            tc_grade      = st.text_input("Pay Grade", placeholder="E-5", key="tc_grade")
            tc_uic        = st.text_input("Unit / UIC", placeholder="USS EXAMPLE (DDG-99) / 12345", key="tc_uic")
        with tc_col2:
            tc_from_date  = st.text_input("Travel From Date", placeholder="2025-03-01", key="tc_from_date")
            tc_to_date    = st.text_input("Travel To Date", placeholder="2025-03-07", key="tc_to_date")
            tc_from_loc   = st.text_input("Departed From", placeholder="Norfolk, VA", key="tc_from_loc")
            tc_to_loc     = st.text_input("Destination", placeholder="San Diego, CA", key="tc_to_loc")

        tc_mode = st.selectbox("Mode of Travel", ["POV (Personal Vehicle)", "Commercial Air", "Government Vehicle", "Rental Car", "Mixed"], key="tc_mode")

        tc_col3, tc_col4 = st.columns(2)
        with tc_col3:
            tc_lodging    = st.text_input("Nightly Lodging Cost ($)", placeholder="e.g. 145.00", key="tc_lodging")
            tc_meals_govt = st.text_input("Government Meals Provided (per day)", placeholder="e.g. 0, 1, or 2", key="tc_meals_govt")
        with tc_col4:
            tc_mileage    = st.text_input("POV Miles Driven (if applicable)", placeholder="e.g. 842", key="tc_mileage")
            tc_advance    = st.text_input("Travel Advance Received ($)", placeholder="e.g. 0.00", key="tc_advance")

        tc_notes = st.text_area(
            "Additional Details / Expenses / Special Circumstances",
            placeholder="Example: Rental car was authorized in orders. Had to purchase $95 gas. GTC used for airfare. One night lodging receipt lost.",
            height=90, key="tc_notes"
        )

        if st.button("Draft Travel Claim Guidance", type="primary", key="gen_travel_claim"):
            if not tc_name.strip() or not tc_from_loc.strip() or not tc_to_loc.strip():
                st.warning("Enter sailor name, departure location, and destination first.")
            else:
                with st.spinner("Drafting travel claim..."):
                    tc_prompt = f"""Draft complete DD 1351-2 travel claim guidance for the following travel. Walk through every applicable block, state what should be entered, calculate per diem where possible, flag any potential errors or missing items, and list all required enclosures.

ORDER TYPE: {tc_order_type}
SAILOR: {tc_name} | Grade: {tc_grade} | Unit/UIC: {tc_uic}
TRAVEL PERIOD: {tc_from_date} to {tc_to_date}
ROUTE: {tc_from_loc} → {tc_to_loc}
MODE: {tc_mode}
LODGING: ${tc_lodging}/night commercial lodging
GOVT MEALS PROVIDED/DAY: {tc_meals_govt}
POV MILES: {tc_mileage}
ADVANCE RECEIVED: ${tc_advance}
ADDITIONAL DETAILS: {tc_notes if tc_notes.strip() else "None"}

Provide:
1. Block-by-block DD 1351-2 instructions with what to enter in each field
2. Per diem calculation (lodging + M&IE, adjusted for govt meals and travel days)
3. Any required DD 1351-6 continuation sheet instructions
4. Required enclosures list
5. Any errors or red flags to address before submission"""

                    response = client.messages.create(
                        model="claude-opus-4-5", max_tokens=4096,
                        system=TRAVEL_SYSTEM_PROMPT,
                        tools=[{"type": "web_search_20250305", "name": "web_search"}],
                        messages=[{"role": "user", "content": tc_prompt}]
                    )
                    tc_out = next((b.text for b in response.content if b.type == "text"), "")
                    st.divider()
                    st.markdown("### Travel Claim Guidance")
                    st.markdown(tc_out)
                    st.download_button(
                        label="📥 Download Travel Claim Guidance",
                        data=tc_out,
                        file_name=f"TravelClaim_{tc_name.replace(' ', '_').replace(',', '')}.txt",
                        mime="text/plain"
                    )

    # ── SECTION 2: DTS HELP ────────────────────────────────────────────────────
    elif travel_section == TRAVEL_SECTIONS[1]:
        st.markdown("#### DTS Help — Defense Travel System")
        st.caption("Get step-by-step DTS guidance for authorizations, vouchers, amendments, and rejections.")

        if "dts_messages" not in st.session_state:
            st.session_state.dts_messages = []

        for msg in st.session_state.dts_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if len(st.session_state.dts_messages) == 0:
            st.markdown("**Common DTS issues:**")
            dts_cols = st.columns(3)
            for i, issue in enumerate(TRAVEL_DTS_ISSUES):
                with dts_cols[i % 3]:
                    if st.button(issue, key=f"dts_quick_{i}"):
                        st.session_state.dts_starter = issue

        if "dts_starter" in st.session_state and st.session_state.dts_starter:
            prompt = st.session_state.dts_starter
            st.session_state.dts_starter = None
            st.session_state.dts_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Looking that up..."):
                    response = client.messages.create(
                        model="claude-opus-4-5", max_tokens=4096,
                        system=TRAVEL_SYSTEM_PROMPT,
                        tools=[{"type": "web_search_20250305", "name": "web_search"}],
                        messages=st.session_state.dts_messages
                    )
                    answer = next((b.text for b in response.content if b.type == "text"), "")
                    st.markdown(answer)
            st.session_state.dts_messages.append({"role": "assistant", "content": answer})
            st.rerun()

        if prompt := st.chat_input("Ask a DTS question...", key="dts_input"):
            st.session_state.dts_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Looking that up..."):
                    response = client.messages.create(
                        model="claude-opus-4-5", max_tokens=4096,
                        system=TRAVEL_SYSTEM_PROMPT,
                        tools=[{"type": "web_search_20250305", "name": "web_search"}],
                        messages=st.session_state.dts_messages
                    )
                    answer = next((b.text for b in response.content if b.type == "text"), "")
                    st.markdown(answer)
            st.session_state.dts_messages.append({"role": "assistant", "content": answer})
            st.rerun()

        if st.button("Clear DTS Chat", key="clear_dts"):
            st.session_state.dts_messages = []
            st.rerun()

    # ── SECTION 3: NROWS ──────────────────────────────────────────────────────
    elif travel_section == TRAVEL_SECTIONS[2]:
        st.markdown("#### NROWS — Navy Reserve Order Writing System")
        st.caption("Step-by-step guidance on writing, routing, and amending reserve orders in NROWS.")

        if "nrows_messages" not in st.session_state:
            st.session_state.nrows_messages = []

        for msg in st.session_state.nrows_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if len(st.session_state.nrows_messages) == 0:
            st.markdown("**Common NROWS issues:**")
            nrows_cols = st.columns(3)
            for i, issue in enumerate(TRAVEL_NROWS_ISSUES):
                with nrows_cols[i % 3]:
                    if st.button(issue, key=f"nrows_quick_{i}"):
                        st.session_state.nrows_starter = issue

        if "nrows_starter" in st.session_state and st.session_state.nrows_starter:
            prompt = st.session_state.nrows_starter
            st.session_state.nrows_starter = None
            st.session_state.nrows_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Looking that up..."):
                    response = client.messages.create(
                        model="claude-opus-4-5", max_tokens=4096,
                        system=TRAVEL_SYSTEM_PROMPT,
                        tools=[{"type": "web_search_20250305", "name": "web_search"}],
                        messages=st.session_state.nrows_messages
                    )
                    answer = next((b.text for b in response.content if b.type == "text"), "")
                    st.markdown(answer)
            st.session_state.nrows_messages.append({"role": "assistant", "content": answer})
            st.rerun()

        if prompt := st.chat_input("Ask an NROWS question...", key="nrows_input"):
            st.session_state.nrows_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Looking that up..."):
                    response = client.messages.create(
                        model="claude-opus-4-5", max_tokens=4096,
                        system=TRAVEL_SYSTEM_PROMPT,
                        tools=[{"type": "web_search_20250305", "name": "web_search"}],
                        messages=st.session_state.nrows_messages
                    )
                    answer = next((b.text for b in response.content if b.type == "text"), "")
                    st.markdown(answer)
            st.session_state.nrows_messages.append({"role": "assistant", "content": answer})
            st.rerun()

        if st.button("Clear NROWS Chat", key="clear_nrows"):
            st.session_state.nrows_messages = []
            st.rerun()

    # ── SECTION 4: PER DIEM ───────────────────────────────────────────────────
    elif travel_section == TRAVEL_SECTIONS[3]:
        st.markdown("#### Per Diem — Rates and M&IE Calculator")
        st.caption("Get per diem rate guidance and M&IE calculations for CONUS and OCONUS travel.")

        pd_col1, pd_col2 = st.columns(2)
        with pd_col1:
            pd_location   = st.text_input("TDY / Training Location", placeholder="e.g. San Diego, CA or Yokosuka, Japan", key="pd_location")
            pd_order_type = st.selectbox("Order Type", TRAVEL_ORDER_TYPES, key="pd_order_type")
            pd_nights     = st.number_input("Number of Nights", min_value=0, max_value=365, value=5, key="pd_nights")
        with pd_col2:
            pd_travel_days = st.number_input("Travel Days (first/last at 75%)", min_value=0, max_value=10, value=2, key="pd_travel_days")
            pd_govt_meals  = st.selectbox("Government Meals Provided Per Day", [0, 1, 2, 3], key="pd_govt_meals")
            pd_lodging_actual = st.text_input("Actual Nightly Lodging Cost ($)", placeholder="e.g. 139.00", key="pd_lodging_actual")

        pd_notes = st.text_area("Any additional details", placeholder="Example: Gov quarters were available but full — denied in writing. Reserve AT orders. Fly-in on Day 1.", height=70, key="pd_notes")

        if st.button("Calculate Per Diem", type="primary", key="gen_per_diem"):
            if not pd_location.strip():
                st.warning("Enter TDY/training location first.")
            else:
                with st.spinner("Calculating per diem..."):
                    pd_prompt = f"""Calculate the per diem entitlement for the following travel. Show your work step by step.

LOCATION: {pd_location}
ORDER TYPE: {pd_order_type}
TRAVEL NIGHTS: {pd_nights}
TRAVEL DAYS (75% M&IE days): {pd_travel_days}
GOVERNMENT MEALS PROVIDED PER DAY: {pd_govt_meals} meals
ACTUAL LODGING COST PER NIGHT: ${pd_lodging_actual if pd_lodging_actual.strip() else "Unknown — use standard rate"}
ADDITIONAL DETAILS: {pd_notes if pd_notes.strip() else "None"}

Provide:
1. Applicable per diem rate for this location (note if CONUS/OCONUS and cite GSA or PDTATAC)
2. Lodging entitlement calculation (actual cost vs. cap)
3. M&IE calculation — full days vs. 75% travel days
4. Government meal deductions if applicable
5. Total per diem entitlement for the entire trip
6. Any flags or issues to be aware of (e.g., government quarters available, rate lookup needed)"""

                    response = client.messages.create(
                        model="claude-opus-4-5", max_tokens=4096,
                        system=TRAVEL_SYSTEM_PROMPT,
                        tools=[{"type": "web_search_20250305", "name": "web_search"}],
                        messages=[{"role": "user", "content": pd_prompt}]
                    )
                    pd_out = next((b.text for b in response.content if b.type == "text"), "")
                    st.divider()
                    st.markdown(f"### Per Diem — {pd_location}")
                    st.markdown(pd_out)
                    st.caption("⚠️ Verify exact rates at GSA.gov (CONUS) or PDTATAC (OCONUS) before submitting your claim.")
                    st.download_button(
                        label="📥 Download Per Diem Calculation",
                        data=pd_out,
                        file_name=f"PerDiem_{pd_location.replace(' ', '_').replace(',', '')}.txt",
                        mime="text/plain"
                    )

    # ── SECTION 5: NSIPS / MMPA ───────────────────────────────────────────────
    elif travel_section == TRAVEL_SECTIONS[4]:
        st.markdown("#### NSIPS / MMPA — Travel Transactions & Pay Account")
        st.caption("Guidance on travel-related NSIPS entries, MMPA debts, DLA, BAH changes, and DFAS reconciliation.")

        if "mmpa_messages" not in st.session_state:
            st.session_state.mmpa_messages = []

        for msg in st.session_state.mmpa_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if len(st.session_state.mmpa_messages) == 0:
            st.markdown("**Common NSIPS/MMPA travel issues:**")
            mmpa_cols = st.columns(3)
            for i, issue in enumerate(TRAVEL_MMPA_ISSUES):
                with mmpa_cols[i % 3]:
                    if st.button(issue, key=f"mmpa_quick_{i}"):
                        st.session_state.mmpa_starter = issue

        if "mmpa_starter" in st.session_state and st.session_state.mmpa_starter:
            prompt = st.session_state.mmpa_starter
            st.session_state.mmpa_starter = None
            st.session_state.mmpa_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Looking that up..."):
                    response = client.messages.create(
                        model="claude-opus-4-5", max_tokens=4096,
                        system=TRAVEL_SYSTEM_PROMPT,
                        tools=[{"type": "web_search_20250305", "name": "web_search"}],
                        messages=st.session_state.mmpa_messages
                    )
                    answer = next((b.text for b in response.content if b.type == "text"), "")
                    st.markdown(answer)
            st.session_state.mmpa_messages.append({"role": "assistant", "content": answer})
            st.rerun()

        if prompt := st.chat_input("Ask an NSIPS or MMPA travel question...", key="mmpa_input"):
            st.session_state.mmpa_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Looking that up..."):
                    response = client.messages.create(
                        model="claude-opus-4-5", max_tokens=4096,
                        system=TRAVEL_SYSTEM_PROMPT,
                        tools=[{"type": "web_search_20250305", "name": "web_search"}],
                        messages=st.session_state.mmpa_messages
                    )
                    answer = next((b.text for b in response.content if b.type == "text"), "")
                    st.markdown(answer)
            st.session_state.mmpa_messages.append({"role": "assistant", "content": answer})
            st.rerun()

        if st.button("Clear NSIPS/MMPA Chat", key="clear_mmpa"):
            st.session_state.mmpa_messages = []
            st.rerun()

    # ── SECTION 6: ASK TRAVEL AGENT ───────────────────────────────────────────
    elif travel_section == TRAVEL_SECTIONS[5]:
        st.markdown("#### Ask Travel Agent")
        st.caption("Open chat with your AI Travel Agent — JTR, DD 1351-2, DTS, NROWS, per diem, and more.")

        if "travel_messages" not in st.session_state:
            st.session_state.travel_messages = []

        for msg in st.session_state.travel_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if len(st.session_state.travel_messages) == 0:
            st.markdown("**Common travel questions:**")
            tq_col1, tq_col2 = st.columns(2)
            with tq_col1:
                if st.button("What are my PCS travel entitlements?"):
                    st.session_state.travel_starter = "What are my PCS travel entitlements as an Active Duty sailor?"
                if st.button("How do I claim IDTT as a Reservist?"):
                    st.session_state.travel_starter = "How do I claim IDTT travel as a Navy Reservist? What are the rules and how do I fill out the DD 1351-2?"
            with tq_col2:
                if st.button("What receipts are required for my claim?"):
                    st.session_state.travel_starter = "What receipts are required to submit a travel claim on DD 1351-2?"
                if st.button("How does split disbursement work?"):
                    st.session_state.travel_starter = "How does split disbursement work for GTC on a DTS travel voucher?"

        if "travel_starter" in st.session_state and st.session_state.travel_starter:
            prompt = st.session_state.travel_starter
            st.session_state.travel_starter = None
            st.session_state.travel_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Looking that up..."):
                    response = client.messages.create(
                        model="claude-opus-4-5", max_tokens=4096,
                        system=TRAVEL_SYSTEM_PROMPT,
                        tools=[{"type": "web_search_20250305", "name": "web_search"}],
                        messages=st.session_state.travel_messages
                    )
                    answer = next((b.text for b in response.content if b.type == "text"), "")
                    st.markdown(answer)
            st.session_state.travel_messages.append({"role": "assistant", "content": answer})
            st.rerun()

        if prompt := st.chat_input("Ask any travel question...", key="travel_input"):
            st.session_state.travel_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Looking that up..."):
                    response = client.messages.create(
                        model="claude-opus-4-5", max_tokens=4096,
                        system=TRAVEL_SYSTEM_PROMPT,
                        tools=[{"type": "web_search_20250305", "name": "web_search"}],
                        messages=st.session_state.travel_messages
                    )
                    answer = next((b.text for b in response.content if b.type == "text"), "")
                    st.markdown(answer)
            st.session_state.travel_messages.append({"role": "assistant", "content": answer})
            st.rerun()

        if st.button("Clear Travel Chat", key="clear_travel"):
            st.session_state.travel_messages = []
            st.rerun()

with st.sidebar:
    st.header("⚓ PS Agent")
    st.markdown(f"**Access:** {access_label.get(st.session_state.access_type, 'User')}")
    st.markdown("**Version:** 1.0 Beta")
    st.markdown("**By:** Strategic Sailor")
    st.divider()
    st.markdown("✅ Reenlistments & Extensions")
    st.markdown("✅ Separations & Discharges")
    st.markdown("✅ Awards & Evals")
    st.markdown("✅ DD Forms")
    st.markdown("✅ MILPERSMAN Citations")
    st.markdown("✅ Humanitarian & Hardship")
    st.divider()
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    if st.button("Log Out"):
        st.session_state.access_granted = False
        st.session_state.access_type = None
        st.session_state.messages = []
        st.rerun()