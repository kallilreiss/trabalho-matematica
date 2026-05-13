import streamlit as st
import random
import time

st.set_page_config(page_title="Poker Financeiro", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:wght@400;500;700&family=IBM+Plex+Sans:wght@400;500;700&display=swap');

.stApp {
    background-color: #080c08;
    background-image:
        radial-gradient(ellipse 60% 40% at 50% 0%, rgba(34,100,34,0.12) 0%, transparent 70%),
        repeating-linear-gradient(0deg, transparent, transparent 40px, rgba(255,255,255,0.01) 40px, rgba(255,255,255,0.01) 41px),
        repeating-linear-gradient(90deg, transparent, transparent 40px, rgba(255,255,255,0.01) 40px, rgba(255,255,255,0.01) 41px);
    color: #c8d4c0;
    font-family: 'IBM Plex Sans', sans-serif;
}
.block-container { max-width: 680px; margin: auto; padding: 2rem 1.5rem; }

h1,h2,h3 { font-family: 'Bebas Neue', sans-serif; letter-spacing: 2px; color: #e8f0e0; }

.stButton > button {
    background: linear-gradient(180deg, #1a4a1a, #0f2e0f);
    color: #80e080;
    border: 1px solid #2a6a2a;
    border-radius: 4px;
    padding: 0.6rem 1.6rem;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    transition: all 0.15s;
    width: 100%;
}
.stButton > button:hover {
    background: linear-gradient(180deg, #225a22, #163616);
    border-color: #40a040;
    box-shadow: 0 0 20px rgba(64,160,64,0.3);
    transform: translateY(-1px);
}
.stTextInput input {
    background: #0a100a !important;
    color: #80e080 !important;
    border: 1px solid #1a3a1a !important;
    border-radius: 3px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 1.2rem !important;
    text-align: center !important;
}
.stTextInput input:focus {
    border-color: #40a040 !important;
    box-shadow: 0 0 0 2px rgba(64,160,64,0.2) !important;
}
.stSlider > div > div > div { background: #40a040 !important; }
.stSlider > div > div { background: #1a2a1a !important; }
.stProgress > div > div { background: linear-gradient(90deg, #1a6a1a, #40e040); }
.stProgress > div { background: #0a180a; border-radius: 2px; }
hr { border-color: #1a2a1a; margin: 1.2rem 0; }

/* MESA DE POKER */
.mesa {
    background: radial-gradient(ellipse at center, #0d2010 0%, #081408 100%);
    border: 2px solid #1a3a1a;
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: inset 0 2px 20px rgba(0,0,0,0.5), 0 0 40px rgba(0,80,0,0.1);
}
.pote-display {
    text-align: center;
    padding: 1rem;
    background: #060e06;
    border: 1px solid #2a4a2a;
    border-radius: 8px;
    margin: 0.8rem 0;
}
.pote-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    color: #3a6a3a;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.pote-valor {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3rem;
    color: #ffd700;
    letter-spacing: 2px;
    line-height: 1;
    text-shadow: 0 0 20px rgba(255,215,0,0.4);
}
.jogador-card {
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin: 0.4rem 0;
}
.j1 {
    background: linear-gradient(135deg, #0a0f18, #0d1520);
    border: 1px solid #1a3060;
}
.j2 {
    background: linear-gradient(135deg, #180a0a, #200d0d);
    border: 1px solid #601a1a;
}
.j-nome {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.j1 .j-nome { color: #4080d0; }
.j2 .j-nome { color: #d04040; }
.j-saldo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    letter-spacing: 1px;
    line-height: 1;
}
.j1 .j-saldo { color: #60a0f0; }
.j2 .j-saldo { color: #f06060; }
.j-aposta {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    margin-top: 0.2rem;
}
.j1 .j-aposta { color: #2a5a90; }
.j2 .j-aposta { color: #902a2a; }

.chip {
    display: inline-block;
    background: #ffd700;
    color: #0a0a08;
    border-radius: 50%;
    width: 28px;
    height: 28px;
    line-height: 28px;
    text-align: center;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    margin: 0 2px;
}

.pergunta-box {
    background: #060e06;
    border: 1px solid #1a3a1a;
    border-left: 3px solid #40a040;
    border-radius: 6px;
    padding: 1.4rem 1.6rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.95rem;
    line-height: 1.9;
    white-space: pre-wrap;
    color: #a0d0a0;
    margin: 0.8rem 0;
}
.status-box {
    background: #060e06;
    border: 1px solid #1a3a1a;
    border-radius: 6px;
    padding: 0.8rem 1.2rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    color: #4a8a4a;
    margin: 0.5rem 0;
    text-align: center;
}
.rodada-badge {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    color: #2a5a2a;
    text-transform: uppercase;
    margin-bottom: 1rem;
    display: block;
}
.nivel-badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 3px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.n1 { background:#0a180a; color:#40c040; border:1px solid #205020; }
.n2 { background:#181800; color:#c0c040; border:1px solid #505020; }
.n3 { background:#180800; color:#c08040; border:1px solid #503010; }
.n4 { background:#180400; color:#e05020; border:1px solid #601808; }
.n5 { background:#180000; color:#e03030; border:1px solid #601010; }

.resultado-acerto {
    background: #081808;
    border: 1px solid #206020;
    border-radius: 8px;
    padding: 1.4rem;
    text-align: center;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    color: #40e040;
    letter-spacing: 2px;
}
.resultado-erro {
    background: #180808;
    border: 1px solid #602020;
    border-radius: 8px;
    padding: 1.4rem;
    text-align: center;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    color: #e04040;
    letter-spacing: 2px;
}
.fold-box {
    background: #100808;
    border: 1px solid #401010;
    border-radius: 6px;
    padding: 0.8rem 1.2rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    color: #804040;
    margin: 0.4rem 0;
}
.ranking-item {
    background: #060e06;
    border: 1px solid #1a2a1a;
    border-radius: 6px;
    padding: 0.7rem 1.1rem;
    margin: 0.35rem 0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.titulo-main {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.5rem;
    letter-spacing: 4px;
    color: #ffd700;
    line-height: 1;
    text-shadow: 0 0 30px rgba(255,215,0,0.3);
}
.subtitulo-main {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 4px;
    color: #2a5a2a;
    text-transform: uppercase;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ─── ESTADO ───────────────────────────────────────────────
if "tela" not in st.session_state:
    st.session_state.tela = "menu"
if "ranking" not in st.session_state:
    st.session_state.ranking = []

# ─── HELPERS ──────────────────────────────────────────────
def nivel_rodada(r):
    return {1:1,2:1,3:2,4:2,5:3,6:3,7:4,8:4,9:5,10:5}.get(r, 3)

def nome_nivel(n):
    return {1:"BÁSICO",2:"SIMPLES",3:"MÉDIO",4:"AVANÇADO",5:"OLITEF"}.get(n,"MÉDIO")

def gerar_pergunta(nivel):
    if nivel == 1:
        v = random.choice([200,400,500,800,1000,1500])
        t = random.choice([10,20,25,50])
        tipo = random.choice(["desconto","acrescimo"])
        if tipo == "desconto":
            res = round(v*(1-t/100))
            q = f"Um produto custa R${v}.\nEstá com {t}% de desconto.\n\nQual é o PREÇO FINAL?"
            exp = f"R${v} × {round(1-t/100,2)} = R${res}"
        else:
            res = round(v*(1+t/100))
            q = f"Um salário de R${v} teve reajuste de {t}%.\n\nQual é o NOVO SALÁRIO?"
            exp = f"R${v} × {round(1+t/100,2)} = R${res}"
        return q, res, exp

    if nivel == 2:
        v = random.choice([1000,2000,3000,5000])
        t = random.choice([5,8,10,12])
        tempo = random.randint(2,6)
        juros = round(v*(t/100)*tempo)
        res = v+juros
        q = (f"Capital de R${v} a {t}% ao mês\n"
             f"em juros SIMPLES por {tempo} meses.\n\n"
             f"Qual é o MONTANTE FINAL?")
        exp = f"J = {v}×{t/100}×{tempo} = R${juros} → M = R${res}"
        return q, res, exp

    if nivel == 3:
        v = random.choice([1000,2000,5000])
        t = random.choice([5,10,15,20])
        tempo = random.randint(2,4)
        res = round(v*((1+t/100)**tempo))
        q = (f"Capital de R${v} a {t}% ao mês\n"
             f"em juros COMPOSTOS por {tempo} meses.\n\n"
             f"Qual é o MONTANTE FINAL?")
        exp = f"M = {v}×(1+{t/100})^{tempo} = R${res}"
        return q, res, exp

    if nivel == 4:
        subtipo = random.choice(["cascata","comparacao"])
        if subtipo == "cascata":
            v = random.choice([2000,4000,5000])
            t1 = random.choice([10,20,25])
            t2 = random.choice([10,15,20])
            res = round(v*(1-t1/100)*(1-t2/100))
            q = (f"Produto custa R${v}.\n"
                 f"1º desconto: {t1}%\n"
                 f"2º desconto (sobre novo preço): {t2}%\n\n"
                 f"Qual é o PREÇO FINAL?")
            exp = f"R${v}×{round(1-t1/100,2)}×{round(1-t2/100,2)} = R${res}"
            return q, res, exp
        else:
            v = random.choice([2000,5000,10000])
            t1 = random.choice([8,10,12])
            t2 = t1+random.choice([2,5])
            tempo1 = random.randint(2,4)
            tempo2 = max(1,tempo1-random.choice([0,1]))
            r1 = round(v*((1+t1/100)**tempo1))
            r2 = round(v*((1+t2/100)**tempo2))
            correta = 1 if r1>r2 else 2
            q = (f"R${v} para investir:\n\n"
                 f"  Opção 1: {t1}% ao mês por {tempo1} meses (comp.)\n"
                 f"  Opção 2: {t2}% ao mês por {tempo2} meses (comp.)\n\n"
                 f"Qual rende MAIS? Digite 1 ou 2.")
            exp = f"Op1→R${r1} | Op2→R${r2} → Opção {correta}"
            return q, correta, exp

    if nivel == 5:
        subtipo = random.choice(["reverso","inflacao","equivalente"])
        if subtipo == "reverso":
            res_final = random.choice([1200,1500,2000,2500,3000])
            t = random.choice([20,25,40,50])
            v = round(res_final/(1-t/100))
            q = (f"Após desconto de {t}%, o preço final foi R${res_final}.\n\n"
                 f"Qual era o PREÇO ORIGINAL?")
            exp = f"R${res_final} ÷ {round(1-t/100,2)} = R${v}"
            return q, v, exp
        if subtipo == "inflacao":
            v = random.choice([1000,2000,3000])
            t = random.choice([5,8,10])
            tempo = random.randint(2,4)
            poder = round(v/((1+t/100)**tempo))
            q = (f"Inflação de {t}% ao ano por {tempo} anos.\n"
                 f"Qual o PODER DE COMPRA real de R${v} hoje\n"
                 f"(em valores atuais)?")
            exp = f"R${v} ÷ (1+{t/100})^{tempo} = R${poder}"
            return q, poder, exp
        v = random.choice([1000,2000,5000])
        t = random.choice([5,8,10])
        tempo = random.choice([2,3,4])
        res = round(v*((1+t/100)**tempo))
        q = (f"Capital de R${v} rende {t}% ao mês\n"
             f"por {tempo} meses (juros compostos).\n\n"
             f"Qual o MONTANTE final?")
        exp = f"M = {v}×(1+{t/100})^{tempo} = R${res}"
        return q, res, exp

    return ("Quanto é 100+200?", 300, "300")

def mostra_jogadores(aposta1=None, aposta2=None, fold1=False, fold2=False):
    s1 = st.session_state.saldo1
    s2 = st.session_state.saldo2
    n1 = st.session_state.nome1
    n2 = st.session_state.nome2
    col1, col2 = st.columns(2)
    with col1:
        ap = f"<div class='j-aposta'>{'FOLD' if fold1 else f'no pote: R${aposta1:,}' if aposta1 else ''}</div>" if (aposta1 or fold1) else ""
        st.markdown(f"""
<div class="jogador-card j1">
    <div class="j-nome">♠ {n1}</div>
    <div class="j-saldo">R${round(s1):,}</div>
    {ap}
</div>""", unsafe_allow_html=True)
    with col2:
        ap = f"<div class='j-aposta'>{'FOLD' if fold2 else f'no pote: R${aposta2:,}' if aposta2 else ''}</div>" if (aposta2 or fold2) else ""
        st.markdown(f"""
<div class="jogador-card j2">
    <div class="j-nome">♥ {n2}</div>
    <div class="j-saldo">R${round(s2):,}</div>
    {ap}
</div>""", unsafe_allow_html=True)

# ─── MENU ─────────────────────────────────────────────────
if st.session_state.tela == "menu":
    st.markdown('<div class="titulo-main">POKER<br>FINANCEIRO</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo-main">duelo de matemática financeira</div>', unsafe_allow_html=True)

    st.markdown("""
<div style="background:#060e06; border:1px solid #1a3a1a; border-radius:8px; padding:1.4rem 1.6rem; margin:1rem 0; font-family:'IBM Plex Mono',monospace; font-size:0.82rem; line-height:2;">
<span style="color:#ffd700; font-family:'Bebas Neue',sans-serif; font-size:1.1rem; letter-spacing:2px;">COMO JOGAR</span><br><br>
Cada jogador começa com <b style="color:#40e040;">R$1.000</b>. São <b style="color:#40e040;">10 rodadas</b>.<br><br>
<span style="color:#ffd700;">① APOSTA 1</span> — Jogador 1 abre com uma aposta. Jogador 2 paga, aumenta ou dá fold.<br>
<span style="color:#ffd700;">② APOSTA 2</span> — Mais uma rodada de apostas (aumentar ou pagar).<br>
<span style="color:#ffd700;">③ PERGUNTA</span> — A pergunta aparece. Os dois digitam a resposta ao mesmo tempo.<br><br>
<span style="color:#2a7a2a;">→ Quem acertar primeiro leva o pote.</span><br>
<span style="color:#2a7a2a;">→ Se acertarem juntos, dividem o pote.</span><br>
<span style="color:#7a2a2a;">→ Fold = perde só o que já apostou.</span><br>
<span style="color:#7a2a2a;">→ Errar = não leva nada (pote fica para próxima rodada!).</span>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div style="font-size:0.65rem;letter-spacing:2px;color:#4080d0;text-transform:uppercase;margin-bottom:0.3rem;">♠ Jogador 1</div>', unsafe_allow_html=True)
        nome1 = st.text_input("nj1", label_visibility="collapsed", placeholder="Nome do Jogador 1", key="inp_n1")
    with col2:
        st.markdown('<div style="font-size:0.65rem;letter-spacing:2px;color:#d04040;text-transform:uppercase;margin-bottom:0.3rem;">♥ Jogador 2</div>', unsafe_allow_html=True)
        nome2 = st.text_input("nj2", label_visibility="collapsed", placeholder="Nome do Jogador 2", key="inp_n2")

    turma = st.text_input("turma", label_visibility="collapsed", placeholder="Turma (ex: 3B)", key="inp_turma")

    if st.button("🃏  EMBARALHAR E COMEÇAR"):
        if not nome1.strip() or not nome2.strip():
            st.warning("Digite os nomes dos dois jogadores.")
            st.stop()
        st.session_state.nome1 = nome1.strip()
        st.session_state.nome2 = nome2.strip()
        st.session_state.turma = turma.strip() or "Sem turma"
        st.session_state.saldo1 = 1000
        st.session_state.saldo2 = 1000
        st.session_state.rodada = 1
        st.session_state.pote_acumulado = 0  # pote que sobra quando ambos erram
        st.session_state.tela = "jogo"
        st.session_state.fase = "aposta1"
        # gera primeira pergunta
        q, r, e = gerar_pergunta(nivel_rodada(1))
        st.session_state.pergunta = q
        st.session_state.resposta_correta = r
        st.session_state.explicacao = e
        st.session_state.aposta_j1 = 0
        st.session_state.aposta_j2 = 0
        st.session_state.fold_j1 = False
        st.session_state.fold_j2 = False
        st.session_state.resp1 = None
        st.session_state.resp2 = None
        st.session_state.resp1_tempo = None
        st.session_state.resp2_tempo = None
        st.rerun()

# ─── JOGO ─────────────────────────────────────────────────
elif st.session_state.tela == "jogo":
    rodada = st.session_state.rodada
    nivel = nivel_rodada(rodada)
    n1 = st.session_state.nome1
    n2 = st.session_state.nome2
    s1 = st.session_state.saldo1
    s2 = st.session_state.saldo2
    pote_ac = st.session_state.pote_acumulado

    # Cabeçalho
    st.markdown(f'<span class="rodada-badge">RODADA {rodada}/10 &nbsp;·&nbsp; <span class="nivel-badge n{nivel}">{nome_nivel(nivel)}</span> &nbsp;·&nbsp; POTE ACUMULADO: R${pote_ac:,}</span>', unsafe_allow_html=True)

    # ── APOSTA 1 ──────────────────────────────────────────
    if st.session_state.fase == "aposta1":
        mostra_jogadores()

        st.markdown('<div class="pote-display"><div class="pote-label">Pote da Rodada</div><div class="pote-valor">R$0</div></div>', unsafe_allow_html=True)

        st.markdown(f"""
<div class="status-box">
    ♠ <b>{n1}</b> abre a aposta &nbsp;—&nbsp; Rodada 1 de 2
</div>
""", unsafe_allow_html=True)

        max_aposta1 = max(10, int(s1 * 0.8))
        aposta1 = st.slider(
            f"Aposta de {n1}:",
            min_value=10,
            max_value=max_aposta1,
            value=min(50, max_aposta1),
            step=10,
            key="sl_ap1"
        )
        st.markdown(f'<div style="text-align:center;font-family:IBM Plex Mono,monospace;font-size:0.8rem;color:#4080d0;margin-top:-0.5rem;margin-bottom:0.8rem;">R${aposta1:,}</div>', unsafe_allow_html=True)

        if st.button(f"♠  {n1.upper()} CONFIRMA APOSTA DE R${aposta1}"):
            st.session_state.aposta_j1 = aposta1
            st.session_state.saldo1 -= aposta1
            st.session_state.fase = "resposta_aposta1"
            st.rerun()

    # ── RESPOSTA DO J2 À APOSTA 1 ─────────────────────────
    elif st.session_state.fase == "resposta_aposta1":
        ap1 = st.session_state.aposta_j1
        mostra_jogadores(aposta1=ap1)

        pote_atual = ap1 + st.session_state.pote_acumulado
        st.markdown(f'<div class="pote-display"><div class="pote-label">Pote da Rodada</div><div class="pote-valor">R${pote_atual:,}</div></div>', unsafe_allow_html=True)

        st.markdown(f"""
<div class="status-box">
    ♥ <b>{n2}</b>: pagar R${ap1} · aumentar · ou fold
</div>
""", unsafe_allow_html=True)

        max_aumento = max(ap1, int(s2 * 0.8))
        acao_j2 = st.radio(
            f"O que {n2} faz?",
            [f"PAGAR (R${ap1})", "AUMENTAR", "FOLD"],
            key="acao_j2_r1",
            horizontal=True
        )

        valor_aumento = ap1
        if "AUMENTAR" in acao_j2:
            valor_aumento = st.slider(
                "Aumentar para:",
                min_value=ap1 + 10,
                max_value=max(ap1 + 10, int(s2 * 0.8)),
                value=min(ap1 * 2, max(ap1 + 10, int(s2 * 0.8))),
                step=10,
                key="sl_aumento1"
            )
            st.markdown(f'<div style="text-align:center;font-family:IBM Plex Mono,monospace;font-size:0.8rem;color:#d04040;margin-top:-0.5rem;margin-bottom:0.8rem;">R${valor_aumento:,}</div>', unsafe_allow_html=True)

        if st.button(f"♥  {n2.upper()} CONFIRMA"):
            if "FOLD" in acao_j2:
                # J2 dá fold — J1 recupera aposta, pote segue sem a aposta do J1
                st.session_state.saldo1 += ap1  # devolve pra J1
                st.session_state.fold_j2 = True
                st.session_state.fase = "resultado_fold"
                st.session_state.fold_vencedor = 1
            elif "PAGAR" in acao_j2:
                st.session_state.aposta_j2 = ap1
                st.session_state.saldo2 -= ap1
                st.session_state.fase = "aposta2"
            else:  # AUMENTAR
                # J2 aumentou — J1 precisa responder
                st.session_state.aposta_j2 = valor_aumento
                st.session_state.saldo2 -= valor_aumento
                st.session_state.fase = "resposta_aumento_j1"
            st.rerun()

    # ── J1 RESPONDE AO AUMENTO ────────────────────────────
    elif st.session_state.fase == "resposta_aumento_j1":
        ap1 = st.session_state.aposta_j1
        ap2 = st.session_state.aposta_j2
        diferenca = ap2 - ap1
        mostra_jogadores(aposta1=ap1, aposta2=ap2)

        pote_atual = ap1 + ap2 + st.session_state.pote_acumulado
        st.markdown(f'<div class="pote-display"><div class="pote-label">Pote da Rodada</div><div class="pote-valor">R${pote_atual:,}</div></div>', unsafe_allow_html=True)

        st.markdown(f"""
<div class="status-box">
    ♥ {n2} aumentou! ♠ <b>{n1}</b>: pagar mais R${diferenca} ou fold
</div>
""", unsafe_allow_html=True)

        acao_j1 = st.radio(
            f"O que {n1} faz?",
            [f"PAGAR (mais R${diferenca})", "FOLD"],
            key="acao_j1_aumento",
            horizontal=True
        )

        if st.button(f"♠  {n1.upper()} CONFIRMA"):
            if "FOLD" in acao_j1:
                # J1 dá fold — perde o que apostou, J2 recupera aposta
                st.session_state.saldo2 += ap2
                st.session_state.fold_j1 = True
                st.session_state.fase = "resultado_fold"
                st.session_state.fold_vencedor = 2
            else:
                st.session_state.saldo1 -= diferenca
                st.session_state.aposta_j1 = ap2  # igualou
                st.session_state.fase = "aposta2"
            st.rerun()

    # ── APOSTA 2 ──────────────────────────────────────────
    elif st.session_state.fase == "aposta2":
        ap1 = st.session_state.aposta_j1
        ap2 = st.session_state.aposta_j2
        pote_atual = ap1 + ap2 + st.session_state.pote_acumulado
        mostra_jogadores(aposta1=ap1, aposta2=ap2)

        st.markdown(f'<div class="pote-display"><div class="pote-label">Pote da Rodada</div><div class="pote-valor">R${pote_atual:,}</div></div>', unsafe_allow_html=True)

        st.markdown(f"""
<div class="status-box">
    ♥ <b>{n2}</b> abre a 2ª aposta &nbsp;—&nbsp; Rodada 2 de 2
</div>
""", unsafe_allow_html=True)

        max_ap2 = max(10, int(s2 * 0.8))
        aposta2_extra = st.slider(
            f"2ª aposta de {n2}:",
            min_value=0,
            max_value=max_ap2,
            value=min(30, max_ap2),
            step=10,
            key="sl_ap2"
        )

        opcoes = ["PASSAR (R$0)"] if aposta2_extra == 0 else [f"APOSTAR R${aposta2_extra}"]

        if st.button(f"♥  {n2.upper()} CONFIRMA"):
            if aposta2_extra > 0:
                st.session_state.aposta_j2 += aposta2_extra
                st.session_state.saldo2 -= aposta2_extra
                st.session_state.fase = "resposta_aposta2"
            else:
                # passou — vai direto pra pergunta
                st.session_state.fase = "pergunta"
            st.rerun()

    # ── RESPOSTA DO J1 À APOSTA 2 ─────────────────────────
    elif st.session_state.fase == "resposta_aposta2":
        ap1 = st.session_state.aposta_j1
        ap2 = st.session_state.aposta_j2
        diferenca = ap2 - ap1
        pote_atual = ap1 + ap2 + st.session_state.pote_acumulado
        mostra_jogadores(aposta1=ap1, aposta2=ap2)

        st.markdown(f'<div class="pote-display"><div class="pote-label">Pote da Rodada</div><div class="pote-valor">R${pote_atual:,}</div></div>', unsafe_allow_html=True)

        st.markdown(f"""
<div class="status-box">
    ♥ {n2} apostou mais! ♠ <b>{n1}</b>: pagar R${max(0,diferenca)} ou fold
</div>
""", unsafe_allow_html=True)

        diff = max(0, ap2 - ap1)
        acao = st.radio(
            f"O que {n1} faz?",
            [f"PAGAR (R${diff})" if diff > 0 else "PAGAR (já igualado)", "FOLD"],
            key="acao_j1_r2",
            horizontal=True
        )

        if st.button(f"♠  {n1.upper()} CONFIRMA"):
            if "FOLD" in acao:
                st.session_state.saldo2 += ap2
                st.session_state.fold_j1 = True
                st.session_state.fase = "resultado_fold"
                st.session_state.fold_vencedor = 2
            else:
                if diff > 0:
                    st.session_state.saldo1 -= diff
                    st.session_state.aposta_j1 = ap2
                st.session_state.fase = "pergunta"
            st.rerun()

    # ── RESULTADO DO FOLD ─────────────────────────────────
    elif st.session_state.fase == "resultado_fold":
        venc = st.session_state.fold_vencedor
        nome_v = n1 if venc == 1 else n2
        ap1 = st.session_state.aposta_j1
        ap2 = st.session_state.aposta_j2
        pote_perdido = (ap2 if venc == 1 else ap1)

        mostra_jogadores(
            fold1=(venc == 2),
            fold2=(venc == 1)
        )

        st.markdown(f"""
<div class="fold-box">
    ✗ {"♥ "+n2 if venc==1 else "♠ "+n1} deu FOLD — perdeu R${pote_perdido:,}
</div>
""", unsafe_allow_html=True)

        st.markdown(f"""
<div class="resultado-acerto">
    {("♠ " if venc==1 else "♥ ") + nome_v.upper()} VENCEU O FOLD<br>
    <span style="font-size:1rem; color:#80c080;">+R${pote_perdido:,}</span>
</div>
""", unsafe_allow_html=True)

        # vencedor do fold ganha o que o perdedor apostou
        if venc == 1:
            st.session_state.saldo1 += pote_perdido
        else:
            st.session_state.saldo2 += pote_perdido

        st.info(f"💡 Pergunta que ninguém respondeu: {st.session_state.pergunta}\n\nResposta: {st.session_state.resposta_correta} — {st.session_state.explicacao}")

        if st.button("▶  PRÓXIMA RODADA"):
            st.session_state.rodada += 1
            if st.session_state.rodada > 10:
                st.session_state.tela = "final"
            else:
                nivel_novo = nivel_rodada(st.session_state.rodada)
                q, r, e = gerar_pergunta(nivel_novo)
                st.session_state.pergunta = q
                st.session_state.resposta_correta = r
                st.session_state.explicacao = e
                st.session_state.aposta_j1 = 0
                st.session_state.aposta_j2 = 0
                st.session_state.fold_j1 = False
                st.session_state.fold_j2 = False
                st.session_state.resp1 = None
                st.session_state.resp2 = None
                st.session_state.resp1_tempo = None
                st.session_state.resp2_tempo = None
                st.session_state.fase = "aposta1"
            st.rerun()

    # ── PERGUNTA ──────────────────────────────────────────
    elif st.session_state.fase == "pergunta":
        ap1 = st.session_state.aposta_j1
        ap2 = st.session_state.aposta_j2
        pote_rodada = ap1 + ap2
        pote_total = pote_rodada + pote_ac
        mostra_jogadores(aposta1=ap1, aposta2=ap2)

        st.markdown(f'<div class="pote-display"><div class="pote-label">🏆 Pote Total em Jogo</div><div class="pote-valor">R${pote_total:,}</div></div>', unsafe_allow_html=True)

        st.markdown(f'<div style="font-size:0.65rem;letter-spacing:2px;color:#2a5a2a;text-transform:uppercase;margin-bottom:0.3rem;">Pergunta da rodada</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="pergunta-box">{st.session_state.pergunta}</div>', unsafe_allow_html=True)

        st.markdown(f"""
<div class="status-box">
    Quem acertar PRIMEIRO leva R${pote_total:,} &nbsp;|&nbsp; Empate = divide &nbsp;|&nbsp; Ambos erram = pote acumula!
</div>
""", unsafe_allow_html=True)

        # Respostas dos dois
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div style="font-size:0.65rem;letter-spacing:2px;color:#4080d0;text-transform:uppercase;margin-bottom:0.3rem;">♠ {n1}</div>', unsafe_allow_html=True)
            resp1_input = st.text_input("r1", label_visibility="collapsed", placeholder="Resposta...", key="resp1_input")
        with col2:
            st.markdown(f'<div style="font-size:0.65rem;letter-spacing:2px;color:#d04040;text-transform:uppercase;margin-bottom:0.3rem;">♥ {n2}</div>', unsafe_allow_html=True)
            resp2_input = st.text_input("r2", label_visibility="collapsed", placeholder="Resposta...", key="resp2_input")

        if st.button("🃏  REVELAR RESPOSTAS"):
            try:
                r1 = int(resp1_input.strip()) if resp1_input.strip() else None
            except:
                r1 = None
            try:
                r2 = int(resp2_input.strip()) if resp2_input.strip() else None
            except:
                r2 = None

            gabarito = st.session_state.resposta_correta
            c1 = r1 is not None and (r1 == gabarito or abs(r1 - gabarito) <= 1)
            c2 = r2 is not None and (r2 == gabarito or abs(r2 - gabarito) <= 1)

            st.session_state.fase = "resultado_pergunta"
            st.session_state.c1 = c1
            st.session_state.c2 = c2
            st.session_state.r1_digitado = r1
            st.session_state.r2_digitado = r2
            st.rerun()

    # ── RESULTADO DA PERGUNTA ─────────────────────────────
    elif st.session_state.fase == "resultado_pergunta":
        ap1 = st.session_state.aposta_j1
        ap2 = st.session_state.aposta_j2
        pote_rodada = ap1 + ap2
        pote_total = pote_rodada + pote_ac
        c1 = st.session_state.c1
        c2 = st.session_state.c2
        r1d = st.session_state.r1_digitado
        r2d = st.session_state.r2_digitado
        gabarito = st.session_state.resposta_correta

        mostra_jogadores(aposta1=ap1, aposta2=ap2)
        st.markdown(f'<div class="pote-display"><div class="pote-label">🏆 Pote em Disputa</div><div class="pote-valor">R${pote_total:,}</div></div>', unsafe_allow_html=True)

        # Mostra respostas
        col1, col2 = st.columns(2)
        with col1:
            cor = "#40e040" if c1 else "#e04040"
            simbolo = "✓" if c1 else "✗"
            st.markdown(f'<div style="text-align:center; padding:0.8rem; background:#060e06; border:1px solid #1a3a1a; border-radius:6px;"><div style="font-size:0.65rem; letter-spacing:2px; color:#4080d0; text-transform:uppercase;">♠ {n1}</div><div style="font-family:Bebas Neue,sans-serif; font-size:2rem; color:{cor};">{simbolo} {r1d if r1d is not None else "—"}</div></div>', unsafe_allow_html=True)
        with col2:
            cor = "#40e040" if c2 else "#e04040"
            simbolo = "✓" if c2 else "✗"
            st.markdown(f'<div style="text-align:center; padding:0.8rem; background:#060e06; border:1px solid #1a3a1a; border-radius:6px;"><div style="font-size:0.65rem; letter-spacing:2px; color:#d04040; text-transform:uppercase;">♥ {n2}</div><div style="font-family:Bebas Neue,sans-serif; font-size:2rem; color:{cor};">{simbolo} {r2d if r2d is not None else "—"}</div></div>', unsafe_allow_html=True)

        st.markdown("")

        if c1 and c2:
            # Empate — divide
            metade = pote_total // 2
            st.session_state.saldo1 += metade
            st.session_state.saldo2 += pote_total - metade
            st.session_state.pote_acumulado = 0
            st.markdown(f'<div class="resultado-acerto">EMPATE! Pote dividido<br><span style="font-size:1rem; color:#80c080;">+R${metade:,} cada</span></div>', unsafe_allow_html=True)
            st.balloons()
        elif c1:
            st.session_state.saldo1 += pote_total
            st.session_state.pote_acumulado = 0
            st.markdown(f'<div class="resultado-acerto">♠ {n1.upper()} ACERTOU!<br><span style="font-size:1rem; color:#80c080;">+R${pote_total:,}</span></div>', unsafe_allow_html=True)
            st.balloons()
        elif c2:
            st.session_state.saldo2 += pote_total
            st.session_state.pote_acumulado = 0
            st.markdown(f'<div class="resultado-acerto">♥ {n2.upper()} ACERTOU!<br><span style="font-size:1rem; color:#80c080;">+R${pote_total:,}</span></div>', unsafe_allow_html=True)
            st.balloons()
        else:
            # Ambos erraram — pote acumula!
            st.session_state.pote_acumulado = pote_total
            st.markdown(f'<div class="resultado-erro">NINGUÉM ACERTOU!<br><span style="font-size:1rem; color:#c08080;">Pote de R${pote_total:,} acumula!</span></div>', unsafe_allow_html=True)

        st.markdown(f'<div style="margin-top:0.8rem;"></div>', unsafe_allow_html=True)
        st.info(f"💡 Gabarito: **{gabarito}** — {st.session_state.explicacao}")

        proximo = "PRÓXIMA RODADA ▶" if rodada < 10 else "VER RESULTADO FINAL ▶"
        if st.button(f"🃏  {proximo}"):
            st.session_state.rodada += 1
            if st.session_state.rodada > 10:
                st.session_state.tela = "final"
            else:
                nivel_novo = nivel_rodada(st.session_state.rodada)
                q, r, e = gerar_pergunta(nivel_novo)
                st.session_state.pergunta = q
                st.session_state.resposta_correta = r
                st.session_state.explicacao = e
                st.session_state.aposta_j1 = 0
                st.session_state.aposta_j2 = 0
                st.session_state.fold_j1 = False
                st.session_state.fold_j2 = False
                st.session_state.resp1 = None
                st.session_state.resp2 = None
                st.session_state.fase = "aposta1"
            st.rerun()

# ─── FINAL ────────────────────────────────────────────────
elif st.session_state.tela == "final":
    n1 = st.session_state.nome1
    n2 = st.session_state.nome2
    s1 = round(st.session_state.saldo1)
    s2 = round(st.session_state.saldo2)

    st.markdown('<div class="titulo-main">FIM DE JOGO</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitulo-main">{st.session_state.turma}</div>', unsafe_allow_html=True)

    if s1 > s2:
        venc, sv, sp, cv = n1, s1, s2, "#60a0f0"
    elif s2 > s1:
        venc, sv, sp, cv = n2, s2, s1, "#f06060"
    else:
        venc = None

    if venc:
        simbolo = "♠" if venc == n1 else "♥"
        st.markdown(f"""
<div style="background:linear-gradient(135deg,#0a1800,#0f2200);border:1px solid #3a6a1a;border-radius:12px;padding:2rem;text-align:center;margin:1rem 0;box-shadow:0 0 40px rgba(64,160,0,0.15);">
    <div style="font-family:IBM Plex Mono,monospace;font-size:0.65rem;letter-spacing:3px;color:#3a6a1a;text-transform:uppercase;margin-bottom:0.5rem;">Vencedor</div>
    <div style="font-family:Bebas Neue,sans-serif;font-size:2.8rem;color:{cv};letter-spacing:3px;">{simbolo} {venc}</div>
    <div style="font-family:Bebas Neue,sans-serif;font-size:2rem;color:#ffd700;margin-top:0.2rem;">R${sv:,}</div>
    <div style="font-family:IBM Plex Mono,monospace;font-size:0.75rem;color:#3a6a1a;margin-top:0.4rem;">sobre R${sp:,} do adversário</div>
</div>
""", unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown(f"""
<div style="background:#0f0f0a;border:1px solid #3a3a1a;border-radius:12px;padding:2rem;text-align:center;margin:1rem 0;">
    <div style="font-family:Bebas Neue,sans-serif;font-size:2rem;color:#ffd700;">EMPATE TOTAL</div>
    <div style="color:#5a5030;font-family:IBM Plex Mono,monospace;">R${s1:,} cada</div>
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        v1 = round(((s1-1000)/1000)*100,1)
        c1 = "#40e040" if v1>=0 else "#e04040"
        st.markdown(f'<div class="jogador-card j1"><div class="j-nome">♠ {n1}</div><div class="j-saldo">R${s1:,}</div><div style="font-size:0.75rem;color:{c1};margin-top:0.2rem;">{"+"+str(v1) if v1>=0 else str(v1)}%</div></div>', unsafe_allow_html=True)
    with col2:
        v2 = round(((s2-1000)/1000)*100,1)
        c2 = "#40e040" if v2>=0 else "#e04040"
        st.markdown(f'<div class="jogador-card j2"><div class="j-nome">♥ {n2}</div><div class="j-saldo">R${s2:,}</div><div style="font-size:0.75rem;color:{c2};margin-top:0.2rem;">{"+"+str(v2) if v2>=0 else str(v2)}%</div></div>', unsafe_allow_html=True)

    # Ranking
    st.session_state.ranking.append({
        "n1": n1, "n2": n2, "turma": st.session_state.turma,
        "s1": s1, "s2": s2,
        "venc": (n1 if s1>s2 else n2 if s2>s1 else "Empate")
    })
    st.session_state.ranking = sorted(st.session_state.ranking, key=lambda x: max(x["s1"],x["s2"]), reverse=True)[:10]

    st.markdown("---")
    st.markdown('<div style="font-size:0.65rem;letter-spacing:2px;color:#2a5a2a;text-transform:uppercase;margin-bottom:0.8rem;">Ranking Geral</div>', unsafe_allow_html=True)
    medalhas = ["①","②","③","④","⑤","⑥","⑦","⑧","⑨","⑩"]
    for i, d in enumerate(st.session_state.ranking):
        destaque = d["n1"]==n1 and d["n2"]==n2
        borda = "border-left:2px solid #ffd700;" if destaque else ""
        st.markdown(f"""
<div class="ranking-item" style="{borda}">
    <span style="color:#2a5a2a;">{medalhas[i]}</span>
    <span style="color:#60a0f0;">♠{d['n1']}</span>
    <span style="color:#4a4a3a;font-size:0.7rem;">vs</span>
    <span style="color:#f06060;">♥{d['n2']}</span>
    <span style="color:#3a5a3a;font-size:0.72rem;margin-left:0.3rem;">({d['turma']})</span>
    <span style="color:#ffd700;margin-left:auto;">🏆 {d['venc']}</span>
</div>
""", unsafe_allow_html=True)

    st.markdown("")
    if st.button("🃏  NOVA PARTIDA"):
        for k in list(st.session_state.keys()):
            if k != "ranking":
                del st.session_state[k]
        st.rerun()