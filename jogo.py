import streamlit as st
import random
import time
import base64

st.set_page_config(page_title="Fique Rico ou Quebre", layout="centered")

# ---------- ESTILO ----------
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: #e5e7eb;
}
.block-container {
    max-width: 700px;
    margin: auto;
    padding: 2rem;
}
h1, h2, h3 {
    color: #f9fafb;
}
.stButton>button {
    background-color: #22c55e;
    color: white;
    border-radius: 8px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ---------- SOM ----------
def tocar_som(file):
    try:
        with open(file, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
            <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
            st.markdown(md, unsafe_allow_html=True)
    except:
        pass

# ---------- ESTADO ----------
if "tela" not in st.session_state:
    st.session_state.tela = "menu"
if "ranking" not in st.session_state:
    st.session_state.ranking = []
if "historico" not in st.session_state:
    st.session_state.historico = []

# ---------- PERGUNTAS AVANÇADAS ----------
def gerar_pergunta(dificuldade):

    v = random.randint(100, 2000)
    t = random.randint(1, 100)  # % aleatória
    tempo = random.randint(1, 4)

    tipo = random.choice([
        "desconto",
        "acrescimo",
        "juros_simples",
        "juros_compostos",
        "comparacao"
    ])

    # ---------- DESCONTO ----------
    if tipo == "desconto":
        res = v*(1-t/100)
        return f"Produto de R${v} com {t}% de desconto → valor final?", round(res,2), f"{v} - {t}% = {res}"

    # ---------- ACRÉSCIMO ----------
    if tipo == "acrescimo":
        res = v*(1+t/100)
        return f"Produto de R${v} com aumento de {t}% → valor final?", round(res,2), f"{v} + {t}% = {res}"

    # ---------- JUROS SIMPLES ----------
    if tipo == "juros_simples":
        res = v*(1 + (t/100)*tempo)
        return f"R${v} a {t}% por {tempo} meses (simples)", round(res,2), f"Total = {res}"

    # ---------- JUROS COMPOSTOS ----------
    if tipo == "juros_compostos":
        res = v*((1+t/100)**tempo)
        return f"R${v} a {t}% por {tempo} meses (composto)", round(res,2), f"Total = {res}"

    # ---------- COMPARAÇÃO (DESAFIO REAL) ----------
    if tipo == "comparacao":
        t1 = random.randint(5, 50)
        t2 = random.randint(5, 50)

        r1 = v*((1+t1/100)**2)
        r2 = v*((1+t2/100)**2)

        correta = 1 if r1 > r2 else 2

        pergunta = f"""
Você tem R${v}

Opção 1: {t1}% por 2 meses  
Opção 2: {t2}% por 2 meses  

Qual dá mais dinheiro? (1 ou 2)
"""
        return pergunta, correta, f"Opção correta: {correta}"

# ---------- MENU ----------
if st.session_state.tela == "menu":

    st.title("💰 Fique Rico ou Quebre")

    st.markdown("""
### 📘 Introdução
- Porcentagem (aumento e desconto)
- Juros simples
- Juros compostos
- Decisão estratégica

🎯 Objetivo: terminar com mais dinheiro
""")

    nome = st.text_input("Nome")
    turma = st.text_input("Turma")
    dificuldade = st.selectbox("Dificuldade", ["Fácil","Médio","Difícil"])
    tempo = st.slider("Tempo por rodada",5,30,15)

    if st.button("🚀 Jogar"):
        st.session_state.nome = nome or "Jogador"
        st.session_state.turma = turma or "Sem turma"
        st.session_state.dificuldade = dificuldade
        st.session_state.tempo = tempo
        st.session_state.dinheiro = 1000
        st.session_state.rodada = 1
        st.session_state.inicio = time.time()
        st.session_state.tela = "jogo"
        st.rerun()

# ---------- JOGO ----------
elif st.session_state.tela == "jogo":

    st.markdown(f"### 💵 R${round(st.session_state.dinheiro,2)} | Rodada {st.session_state.rodada}/10")

    restante = st.session_state.tempo - int(time.time() - st.session_state.inicio)

    if restante <= 0:
        st.error("⏱️ Tempo acabou!")
        st.session_state.dinheiro *= 0.9
        st.session_state.rodada += 1
        st.session_state.inicio = time.time()
        st.rerun()

    st.progress(restante/st.session_state.tempo)
    st.write(f"⏳ {restante}s")

    if "p" not in st.session_state:
        p,r,e = gerar_pergunta(st.session_state.dificuldade)
        st.session_state.p = p
        st.session_state.r = r
        st.session_state.e = e

    st.write(st.session_state.p)

    resp = st.text_input("Resposta:")

    if st.button("Confirmar resposta"):

        try:
            resp_val = float(resp)
        except:
            resp_val = resp

        if resp_val == st.session_state.r or abs(float(resp_val) - float(st.session_state.r)) < 0.1:
            st.success("✅ Acertou! +15%")
            st.session_state.dinheiro *= 1.15
        else:
            st.error(f"❌ Errado! Correto: {st.session_state.r}")
            st.session_state.dinheiro *= 0.85

        st.info(st.session_state.e)
        del st.session_state.p

    acao = st.radio("Escolha:", ["Investir","Guardar","Arriscar"])

    if st.button("Confirmar ação"):
        if acao == "Investir":
            st.session_state.dinheiro *= 1.1

        elif acao == "Arriscar":
            if random.random() > 0.5:
                st.success("📈 Grande lucro!")
                st.session_state.dinheiro *= 1.3
            else:
                st.error("📉 Prejuízo!")
                st.session_state.dinheiro *= 0.7

        st.session_state.rodada += 1
        st.session_state.inicio = time.time()

        if st.session_state.rodada > 10:
            st.session_state.tela = "final"

        st.rerun()

# ---------- FINAL ----------
else:
    d = round(st.session_state.dinheiro,2)

    st.title("🏁 Resultado")

    if d > 2000:
        st.success(f"🤑 Rico! R${d}")
        st.balloons()
    elif d > 1000:
        st.info(f"🙂 Estável R${d}")
    else:
        st.error(f"😬 Endividado R${d}")

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

    st.subheader("🏆 Ranking")
    for i, jogador in enumerate(st.session_state.ranking, 1):
        st.write(f"{i}. {jogador['nome']} ({jogador['turma']}) - R${jogador['dinheiro']}")

    if st.button("🔁 Jogar novamente"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()