import streamlit as st
import random
import time

st.set_page_config(page_title="Fique Rico ou Quebre", layout="centered")

# ---------- ESTILO ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=Space+Mono:wght@400;700&display=swap');

.stApp {
    background-color: #060a10;
    color: #e5e7eb;
    font-family: 'Space Mono', monospace;
}
.block-container {
    max-width: 720px;
    margin: auto;
    padding: 2rem 1.5rem;
}
h1, h2, h3 {
    font-family: 'Syne', sans-serif;
    color: #f0fdf4;
    letter-spacing: -0.5px;
}
.stButton>button {
    background: linear-gradient(135deg, #16a34a, #15803d);
    color: white;
    border-radius: 6px;
    border: none;
    padding: 0.65rem 1.4rem;
    font-weight: 700;
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    transition: all 0.2s;
    letter-spacing: 0.5px;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(34,197,94,0.35);
}
.stTextInput input {
    background-color: #111827;
    color: #e5e7eb;
    border: 1px solid #1f2937;
    border-radius: 6px;
    font-family: 'Space Mono', monospace;
}
.stRadio [role=radiogroup] {
    gap: 0.5rem;
}
.stRadio label {
    color: #d1d5db !important;
    font-size: 0.9rem;
}
.stProgress > div > div {
    background: linear-gradient(90deg, #22c55e, #86efac);
}
.dinheiro-box {
    background: linear-gradient(135deg, #0f2d1a, #14532d);
    border: 1px solid #166534;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
    font-family: 'Syne', sans-serif;
}
.dinheiro-valor {
    font-size: 2.4rem;
    font-weight: 800;
    color: #4ade80;
    letter-spacing: -1px;
}
.rodada-badge {
    background: #1f2937;
    border: 1px solid #374151;
    border-radius: 20px;
    padding: 0.3rem 0.9rem;
    font-size: 0.8rem;
    color: #9ca3af;
    display: inline-block;
    font-family: 'Space Mono', monospace;
}
.diff-badge {
    display: inline-block;
    border-radius: 20px;
    padding: 0.25rem 0.8rem;
    font-size: 0.75rem;
    font-weight: 700;
    font-family: 'Syne', sans-serif;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.diff-1 { background:#1a2e1a; color:#4ade80; border:1px solid #166534; }
.diff-2 { background:#1c2514; color:#a3e635; border:1px solid #365314; }
.diff-3 { background:#2a2008; color:#fbbf24; border:1px solid #92400e; }
.diff-4 { background:#2a1008; color:#f97316; border:1px solid #9a3412; }
.diff-5 { background:#2a0808; color:#f87171; border:1px solid #991b1b; }
.pergunta-box {
    background: #111827;
    border: 1px solid #1f2937;
    border-left: 3px solid #22c55e;
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    margin: 1rem 0;
    font-size: 0.95rem;
    white-space: pre-wrap;
    line-height: 1.7;
}
.acao-box {
    background: #0d1117;
    border: 1px solid #1f2937;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
}
.mercado-info {
    background: #0f172a;
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 0.8rem 1.1rem;
    font-size: 0.82rem;
    color: #93c5fd;
    margin: 0.5rem 0;
}
.evento-box {
    background: #1c1208;
    border: 1px solid #92400e;
    border-radius: 8px;
    padding: 0.8rem 1.1rem;
    margin: 0.5rem 0;
    font-size: 0.85rem;
    color: #fbbf24;
}
.ranking-item {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    margin: 0.4rem 0;
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
}
hr {
    border-color: #1f2937;
    margin: 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# ---------- ESTADO ----------
if "tela" not in st.session_state:
    st.session_state.tela = "menu"
if "ranking" not in st.session_state:
    st.session_state.ranking = []

# ---------- NÍVEL DA RODADA ----------
def nivel_rodada(rodada):
    mapa = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 4, 7: 5, 8: 4, 9: 3, 10: 2}
    return mapa.get(rodada, 3)

def nome_nivel(n):
    nomes = {1: "FÁCIL", 2: "MÉDIO", 3: "DIFÍCIL", 4: "PERIGOSO", 5: "EXTREMO"}
    return nomes.get(n, "MÉDIO")

# ---------- GERAR PERGUNTA ----------
def gerar_pergunta(nivel):
    if nivel == 1:
        v = random.choice([200, 400, 500, 800, 1000, 1200])
        t = random.choice([10, 20, 25, 50])
        tipo = random.choice(["desconto", "acrescimo"])
        if tipo == "desconto":
            res = round(v * (1 - t / 100))
            q = f"Um produto custa R${v}.\nEstá com {t}% de desconto.\n\nQual é o PREÇO FINAL?"
        else:
            res = round(v * (1 + t / 100))
            q = f"Um salário de R${v} teve reajuste de {t}%.\n\nQual é o NOVO SALÁRIO?"
        return q, res, f"Cálculo: R${v} × {1 - t/100 if tipo == 'desconto' else 1 + t/100} = R${res}"

    if nivel == 2:
        v = random.choice([1000, 2000, 3000, 5000])
        t = random.choice([5, 8, 10, 12])
        tempo = random.randint(2, 6)
        juros = round(v * (t / 100) * tempo)
        res = v + juros
        q = f"Você investiu R${v} a {t}% ao mês (juros SIMPLES)\npor {tempo} meses.\n\nQual é o MONTANTE FINAL?"
        return q, res, f"Juros = {v} × {t/100} × {tempo} = R${juros} → Total = R${res}"

    if nivel == 3:
        v = random.choice([1000, 2000, 5000])
        t = random.choice([5, 10, 15, 20])
        tempo = random.randint(2, 4)
        res = round(v * ((1 + t / 100) ** tempo))
        q = f"Capital de R${v} aplicado a {t}% ao mês\n(juros COMPOSTOS) por {tempo} meses.\n\nQual é o MONTANTE FINAL?"
        return q, res, f"M = {v} × (1 + {t/100})^{tempo} = R${res}"

    if nivel == 4:
        v = random.choice([2000, 5000, 10000])
        t1 = random.choice([8, 10, 12])
        t2 = t1 + random.choice([2, 5])
        tempo1 = random.randint(2, 4)
        tempo2 = tempo1 - random.choice([0, 1])
        if tempo2 < 1:
            tempo2 = 1
        r1 = v * ((1 + t1 / 100) ** tempo1)
        r2 = v * ((1 + t2 / 100) ** tempo2)
        correta = 1 if r1 > r2 else 2
        q = (
            f"Você tem R${v} para investir:\n\n"
            f"  Opção 1: {t1}% ao mês por {tempo1} meses (comp.)\n"
            f"  Opção 2: {t2}% ao mês por {tempo2} meses (comp.)\n\n"
            f"Qual opção rende MAIS?\nDigite 1 ou 2."
        )
        return q, correta, (
            f"Opção 1 → R${round(r1)}\n"
            f"Opção 2 → R${round(r2)}\n"
            f"Melhor: Opção {correta}"
        )

    if nivel == 5:
        subtipo = random.choice(["cascata", "reverso", "inflacao"])
        if subtipo == "cascata":
            v = random.choice([2000, 4000, 5000])
            t1 = random.choice([10, 20, 25])
            t2 = random.choice([10, 15, 20])
            res = round(v * (1 - t1 / 100) * (1 - t2 / 100))
            q = (
                f"Um produto custa R${v}.\n"
                f"Primeiro recebe {t1}% de desconto.\n"
                f"Depois mais {t2}% sobre o novo preço.\n\n"
                f"Qual é o PREÇO FINAL?"
            )
            return q, res, f"R${v} × {1-t1/100} × {1-t2/100} = R${res}"

        if subtipo == "reverso":
            res_final = random.choice([1200, 1500, 2000, 2500])
            t = random.choice([20, 25, 50])
            v = round(res_final / (1 - t / 100))
            q = (
                f"Após um desconto de {t}%, o preço final foi R${res_final}.\n\n"
                f"Qual era o PREÇO ORIGINAL?"
            )
            return q, v, f"R${res_final} ÷ {1-t/100} = R${v}"

        # inflação
        v = random.choice([1000, 2000, 3000])
        t = random.choice([5, 8, 10])
        tempo = random.randint(2, 4)
        poder = round(v / ((1 + t / 100) ** tempo))
        q = (
            f"Com inflação de {t}% ao ano por {tempo} anos,\n"
            f"o que R${v} de hoje valem no futuro?\n\n"
            f"Qual é o PODER DE COMPRA real (em reais de hoje)?"
        )
        return q, poder, f"Poder = {v} ÷ (1+{t/100})^{tempo} = R${poder}"

    return ("2 + 2 = ?", 4, "4")

# ---------- EVENTO DE MERCADO ----------
EVENTOS = [
    {"desc": "📉 Crise econômica! Investimentos rendem menos.", "efeito": "baixo_invest"},
    {"desc": "📈 Boom no mercado! Arriscar pode ser muito lucrativo.", "efeito": "alto_risco"},
    {"desc": "🔥 Inflação alta! Guardar dinheiro perde valor.", "efeito": "inflacao"},
    {"desc": "🏦 Banco central sobe juros. Investimentos conservadores rendem mais.", "efeito": "alto_invest"},
    {"desc": "⚠️ Mercado instável. Arriscar pode ser catastrófico.", "efeito": "risco_negativo"},
    {"desc": "🟢 Condições normais de mercado.", "efeito": "normal"},
]

def sortear_evento():
    return random.choice(EVENTOS)

# ---------- CALCULAR AÇÃO ----------
def calcular_acao(acao, dinheiro, evento, acertos_seguidos):
    efeito = evento["efeito"]

    if acao == "Investir (renda fixa ~8%)":
        if efeito == "alto_invest":
            taxa = random.uniform(0.12, 0.18)
            msg = f"🏦 Banco central ajudou! Rendeu {round(taxa*100, 1)}%"
        elif efeito == "baixo_invest":
            taxa = random.uniform(0.02, 0.05)
            msg = f"📉 Crise reduziu o rendimento: {round(taxa*100, 1)}%"
        elif efeito == "inflacao":
            taxa = random.uniform(0.06, 0.09)
            inflacao = random.uniform(0.07, 0.12)
            real = taxa - inflacao
            novo = dinheiro * (1 + real)
            msg = (
                f"🔥 Inflação corroeu o ganho! Nominal: {round(taxa*100,1)}%"
                f", Inflação: {round(inflacao*100,1)}%"
                f"\nGanho REAL: {round(real*100,1)}%"
            )
            return max(novo, dinheiro * 0.95), msg, real > 0
        else:
            taxa = random.uniform(0.07, 0.10)
            msg = f"✅ Rendimento seguro de {round(taxa*100, 1)}%"
        return dinheiro * (1 + taxa), msg, True

    elif acao == "Guardar (sem rendimento)":
        if efeito == "inflacao":
            perda = random.uniform(0.06, 0.10)
            msg = f"🔥 Inflação corroeu {round(perda*100,1)}% do dinheiro guardado!"
            return dinheiro * (1 - perda), msg, False
        else:
            msg = "🔒 Dinheiro guardado em segurança. Sem ganhos, sem perdas."
            return dinheiro, msg, True

    elif acao == "Arriscar (ações/cripto)":
        sorte = random.random()
        chance_sucesso = 0.50
        if efeito == "alto_risco":
            chance_sucesso = 0.65
        elif efeito == "risco_negativo":
            chance_sucesso = 0.30
        elif efeito == "baixo_invest":
            chance_sucesso = 0.40
        chance_sucesso += acertos_seguidos * 0.03
        if sorte < chance_sucesso:
            taxa = random.uniform(0.20, 0.50)
            msg = f"🚀 Aposta certeira! +{round(taxa*100)}% de lucro!"
            return dinheiro * (1 + taxa), msg, True
        else:
            taxa = random.uniform(0.25, 0.55)
            msg = f"💥 Mercado afundou! -{round(taxa*100)}% de prejuízo!"
            return dinheiro * (1 - taxa), msg, False

    elif acao == "Reinvestir (juros compostos ~12%)":
        if efeito in ["alto_invest", "normal", "alto_risco"]:
            taxa = random.uniform(0.10, 0.15)
            msg = f"📈 Reinvestimento composto rendeu {round(taxa*100,1)}%!"
            return dinheiro * (1 + taxa), msg, True
        elif efeito == "inflacao":
            taxa = random.uniform(0.09, 0.13)
            inflacao = random.uniform(0.07, 0.11)
            real = taxa - inflacao
            novo = dinheiro * (1 + real)
            msg = (
                f"📊 Nominal: {round(taxa*100,1)}% | Inflação: {round(inflacao*100,1)}%"
                f"\n→ Ganho real: {round(real*100,1)}%"
            )
            return max(novo, dinheiro * 0.92), msg, real > 0
        else:
            taxa = random.uniform(0.04, 0.08)
            msg = f"📉 Crise reduziu retorno composto para {round(taxa*100,1)}%"
            return dinheiro * (1 + taxa), msg, True

    return dinheiro, "Ação inválida.", True

# ==================== TELAS ====================

# ---------- MENU ----------
if st.session_state.tela == "menu":
    st.markdown('<h1 style="font-size:2.2rem;">💸 Fique Rico ou Quebre</h1>', unsafe_allow_html=True)
    st.markdown("""
<div style="background:#0f1f10; border:1px solid #166534; border-radius:10px; padding:1.2rem 1.5rem; margin:1rem 0;">
<b style="color:#4ade80; font-family:Syne,sans-serif;">🎮 COMO FUNCIONA</b><br><br>
Você começa com <b>R$1.000</b> e joga <b>10 rodadas</b>.<br>
A dificuldade das perguntas <b>sobe até a rodada 6</b> e depois <b>regride</b>.<br><br>
<b>A cada rodada você:</b><br>
1. Responde uma pergunta matemática (acerto = +15%, erro = -15%)<br>
2. Escolhe uma <b>ação financeira</b> estratégica<br>
3. Recebe um <b>evento de mercado</b> que afeta seus ganhos/perdas<br><br>
<b style="color:#4ade80;">💼 As ações financeiras:</b><br>
• <b>Guardar:</b> Seguro — mas inflação pode corroer seu dinheiro<br>
• <b>Investir (renda fixa):</b> Rendimento previsível, sofre com crise<br>
• <b>Reinvestir (juros compostos):</b> Melhor retorno no longo prazo<br>
• <b>Arriscar (ações/cripto):</b> Pode dobrar ou perder metade — depende do mercado<br><br>
⚡ <b>Fique atento aos eventos!</b> Eles mudam tudo.
</div>
""", unsafe_allow_html=True)

    nome = st.text_input("👤 Nome")
    turma = st.text_input("🏫 Turma")
    tempo = st.slider("⏱️ Tempo por rodada (segundos)", 10, 60, 30)

    if st.button("🚀 Começar Jogo"):
        st.session_state.nome = nome or "Jogador"
        st.session_state.turma = turma or "Sem turma"
        st.session_state.tempo = tempo
        st.session_state.dinheiro = 1000
        st.session_state.rodada = 1
        st.session_state.inicio = time.time()
        st.session_state.acertos_seguidos = 0
        st.session_state.evento = sortear_evento()
        st.session_state.tela = "jogo"
        st.rerun()

# ---------- JOGO ----------
elif st.session_state.tela == "jogo":
    rodada = st.session_state.rodada
    nivel = nivel_rodada(rodada)
    dinheiro = st.session_state.dinheiro
    evento = st.session_state.evento

    # Cabeçalho
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f'<span class="rodada-badge">RODADA {rodada}/10</span>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<span class="diff-badge diff-{nivel}">{nome_nivel(nivel)}</span>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<span style="font-size:0.75rem; color:#6b7280;">🔥 {st.session_state.acertos_seguidos} seguidos</span>', unsafe_allow_html=True)

    # Dinheiro
    cor = "#4ade80" if dinheiro >= 1000 else "#f87171"
    st.markdown(f"""
<div class="dinheiro-box">
    <div style="font-size:0.75rem; color:#6b7280; margin-bottom:0.3rem;">SEU PATRIMÔNIO</div>
    <div class="dinheiro-valor" style="color:{cor};">R${round(dinheiro):,}</div>
</div>
""", unsafe_allow_html=True)

    # Evento de mercado
    st.markdown(f'<div class="evento-box">⚡ <b>EVENTO DE MERCADO:</b> {evento["desc"]}</div>', unsafe_allow_html=True)

    # Timer
    restante = st.session_state.tempo - int(time.time() - st.session_state.inicio)
    if restante <= 0:
        st.error("⏰ Tempo esgotado! -10% automático")
        st.session_state.dinheiro *= 0.90
        st.session_state.rodada += 1
        st.session_state.acertos_seguidos = 0
        st.session_state.inicio = time.time()
        st.session_state.evento = sortear_evento()
        if "p" in st.session_state:
            del st.session_state.p
        if st.session_state.rodada > 10:
            st.session_state.tela = "final"
        st.rerun()

    cor_timer = "#4ade80" if restante > st.session_state.tempo * 0.4 else "#f97316" if restante > st.session_state.tempo * 0.2 else "#f87171"
    st.progress(restante / st.session_state.tempo)
    st.markdown(f'<p style="color:{cor_timer}; font-size:0.85rem; font-family:Space Mono,monospace;">⏱️ {restante}s restantes</p>', unsafe_allow_html=True)

    st.markdown("---")

    # ---- FASE 1: PERGUNTA ----
    if "fase" not in st.session_state or st.session_state.fase == "pergunta":
        st.session_state.fase = "pergunta"

        if "p" not in st.session_state:
            p, r, e = gerar_pergunta(nivel)
            st.session_state.p = p
            st.session_state.r = r
            st.session_state.e = e

        st.markdown('<h3 style="font-size:1rem; color:#9ca3af;">🧮 PERGUNTA</h3>', unsafe_allow_html=True)
        st.markdown(f'<div class="pergunta-box">{st.session_state.p}</div>', unsafe_allow_html=True)

        resposta = st.text_input("Sua resposta:", key="resp_input", placeholder="Digite apenas números inteiros")

        if st.button("✅ Confirmar Resposta"):
            try:
                r_user = int(resposta.strip())
            except:
                st.warning("Digite apenas números inteiros!")
                st.stop()

            correto = r_user == st.session_state.r
            if not correto and abs(r_user - st.session_state.r) <= 1:
                correto = True

            if correto:
                st.session_state.dinheiro *= 1.15
                st.session_state.acertos_seguidos += 1
                st.session_state.resp_resultado = ("✅ Correto! +15%", True)
            else:
                st.session_state.dinheiro *= 0.85
                st.session_state.acertos_seguidos = 0
                st.session_state.resp_resultado = (f"❌ Errado! A resposta era R${st.session_state.r}", False)

            st.session_state.fase = "acao"
            if "p" in st.session_state:
                del st.session_state.p
            st.rerun()

    # ---- FASE 2: AÇÃO ----
    elif st.session_state.fase == "acao":
        resultado_msg, acerto = st.session_state.resp_resultado
        if acerto:
            st.success(resultado_msg)
            st.balloons()
        else:
            st.error(resultado_msg)
        st.info(f"💡 {st.session_state.e}")

        st.markdown("---")
        st.markdown('<h3 style="font-size:1rem; color:#9ca3af;">💼 ESTRATÉGIA FINANCEIRA</h3>', unsafe_allow_html=True)

        st.markdown(f"""
<div class="mercado-info">
    <b>Condição atual:</b> {evento["desc"]}<br>
    <span style="font-size:0.78rem; color:#64748b;">Considere o contexto ao escolher sua ação.</span>
</div>
""", unsafe_allow_html=True)

        acao = st.radio(
            "Escolha o que fazer com seu dinheiro:",
            [
                "Guardar (sem rendimento)",
                "Investir (renda fixa ~8%)",
                "Reinvestir (juros compostos ~12%)",
                "Arriscar (ações/cripto)",
            ],
            key="radio_acao"
        )

        dicas = {
            "Guardar (sem rendimento)": "🔒 Proteção máxima, mas inflação pode corroer.",
            "Investir (renda fixa ~8%)": "🏦 Rendimento previsível. Ideal em crise.",
            "Reinvestir (juros compostos ~12%)": "📈 Melhor retorno no longo prazo. Risco moderado.",
            "Arriscar (ações/cripto)": "🎲 Alto ganho potencial. Mas o mercado está imprevisível!",
        }
        st.markdown(f'<div style="font-size:0.82rem; color:#6b7280; margin:0.3rem 0 0.8rem;">{dicas[acao]}</div>', unsafe_allow_html=True)

        if st.button("💰 Confirmar Ação"):
            novo_d, msg_acao, sucesso = calcular_acao(
                acao,
                st.session_state.dinheiro,
                evento,
                st.session_state.acertos_seguidos
            )
            st.session_state.dinheiro = novo_d
            if sucesso:
                st.success(msg_acao)
            else:
                st.error(msg_acao)

            st.session_state.rodada += 1
            st.session_state.inicio = time.time()
            st.session_state.evento = sortear_evento()
            st.session_state.fase = "pergunta"

            if st.session_state.rodada > 10:
                st.session_state.tela = "final"
            st.rerun()

# ---------- FINAL ----------
else:
    d = round(st.session_state.dinheiro)
    st.markdown('<h1 style="font-size:2rem;">🏁 RESULTADO FINAL</h1>', unsafe_allow_html=True)

    if d >= 5000:
        st.success(f"🤑 Milionário! Você terminou com R${d:,}")
        st.balloons()
        estrelas = "⭐⭐⭐⭐⭐"
    elif d >= 3000:
        st.success(f"🎉 Ótimo resultado! R${d:,}")
        estrelas = "⭐⭐⭐⭐"
    elif d >= 1500:
        st.info(f"👍 Resultado razoável. R${d:,}")
        estrelas = "⭐⭐⭐"
    elif d >= 800:
        st.warning(f"😅 Quase faliu... R${d:,}")
        estrelas = "⭐⭐"
    else:
        st.error(f"💀 Falência! R${d:,} — menos do que começou!")
        estrelas = "⭐"

    st.markdown(f'<div style="font-size:1.8rem; margin:0.5rem 0;">{estrelas}</div>', unsafe_allow_html=True)

    variacao = round(((d - 1000) / 1000) * 100, 1)
    cor_v = "#4ade80" if variacao >= 0 else "#f87171"
    sinal = "+" if variacao >= 0 else ""
    st.markdown(f'<p style="color:{cor_v}; font-family:Space Mono,monospace;">Variação: {sinal}{variacao}%</p>', unsafe_allow_html=True)

    # Salvar ranking
    st.session_state.ranking.append({
        "nome": st.session_state.nome,
        "turma": st.session_state.turma,
        "dinheiro": d
    })
    st.session_state.ranking = sorted(
        st.session_state.ranking,
        key=lambda x: x["dinheiro"],
        reverse=True
    )[:10]

    st.markdown("---")
    st.markdown('<h3 style="font-size:1rem; color:#9ca3af;">🏆 RANKING</h3>', unsafe_allow_html=True)

    medalhas = ["🥇", "🥈", "🥉"] + ["🎖️"] * 7
    for i, jogador in enumerate(st.session_state.ranking, 1):
        destaque = jogador["nome"] == st.session_state.nome and jogador["dinheiro"] == d
        borda = "border-left: 3px solid #4ade80;" if destaque else ""
        st.markdown(f"""
<div class="ranking-item" style="{borda}">
    {medalhas[i-1]} <b>{jogador['nome']}</b> <span style="color:#6b7280;">({jogador['turma']})</span>
    <span style="float:right; color:#4ade80;">R${jogador['dinheiro']:,}</span>
</div>
""", unsafe_allow_html=True)

    st.markdown("")
    if st.button("🔄 Jogar Novamente"):
        for k in list(st.session_state.keys()):
            if k != "ranking":
                del st.session_state[k]
        st.rerun()