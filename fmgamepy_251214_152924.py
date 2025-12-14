"""
=============================================================
FÍSICO MÉDICO: A MISSÃO - Jogo Educativo de Física Radiológica
=============================================================

DESCRIÇÃO:
Jogo interativo para aprendizado prático de física radiológica,
medicina nuclear e proteção radiológica.

MÓDULOS:
1. Painel Principal       4. Simuladores
2. Sistema de Missões     5. Perfil e Progresso  
3. Calculadoras           6. Ranking

AUTOR: Sistema de Ensino Radiológico
VERSÃO: 1.0.0
REQUISITOS: streamlit, numpy, matplotlib, pandas

EXECUTAR: streamlit run fisico_medico_jogo.py
=============================================================
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import random
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# ============================================================
# CONFIGURAÇÃO INICIAL E ESTADO DA SESSÃO
# ============================================================

def inicializar_sessao():
    """Inicializa todas as variáveis de sessão do jogo"""
    
    # Estado do jogo
    if 'nivel' not in st.session_state:
        st.session_state.nivel = 1
        st.session_state.xp = 0
        st.session_state.xp_total = 0
        st.session_state.dinheiro = 5000
        st.session_state.reputacao = 50
        st.session_state.missoes_completas = 0
        st.session_state.erros_cometidos = 0
        
    # Habilidades do jogador
    if 'habilidades' not in st.session_state:
        st.session_state.habilidades = {
            'decaimento': {'nivel': 1, 'xp': 0, 'formulas': ['A(t)=A₀×(½)^(t/T)']},
            'dosimetria': {'nivel': 1, 'xp': 0, 'formulas': ['Dose=E/m']},
            'detectores': {'nivel': 1, 'xp': 0, 'formulas': ['Geiger-Müller']},
            'protecao': {'nivel': 1, 'xp': 0, 'formulas': ['Lei 1/r²']},
            'espectrometria': {'nivel': 0, 'xp': 0, 'formulas': []}
        }
    
    # Inventário
    if 'inventario' not in st.session_state:
        st.session_state.inventario = {
            'detectores': {
                'geiger': {'quantidade': 1, 'condicao': 100},
                'camera_ionizacao': {'quantidade': 0, 'condicao': 0},
                'nai': {'quantidade': 0, 'condicao': 0}
            },
            'ferramentas': {
                'calculadora': True,
                'tabela_constantes': True,
                'manual': False
            }
        }
    
    # Progresso nas missões
    if 'progresso_missoes' not in st.session_state:
        st.session_state.progresso_missoes = {}
    
    # Conquistas
    if 'conquistas' not in st.session_state:
        st.session_state.conquistas = {
            'primeiro_calculo': False,
            'detetive_perfeito': False,
            'mestre_dosimetria': False,
            'salvador_vidas': False
        }

# ============================================================
# MÓDULO 1: PAINEL PRINCIPAL
# ============================================================

def mostrar_painel_principal():
    """Exibe o painel principal do jogo"""
    
    st.title("🏥 FÍSICO MÉDICO: A MISSÃO")
    
    # Banner principal
    st.image("https://via.placeholder.com/800x200/1E3A8A/FFFFFF?text=Hospital+Imagin%C3%A1rio+da+Sa%C3%BAde+P%C3%BAblica", 
             use_column_width=True)
    
    # Introdução
    st.markdown("""
    ## 👨‍⚕️ Bem-vindo ao HISP - Hospital Imaginário da Saúde Pública
    
    Você é um **Físico Médico estagiário** iniciando sua carreira no maior 
    centro de referência do país. Sua missão: aprender e aplicar os conceitos 
    de física radiológica para salvar vidas e garantir a segurança.
    
    ### 🎯 Seus Objetivos:
    1. Completar missões em diferentes departamentos
    2. Aprender e aplicar cálculos radiológicos
    3. Escolher os equipamentos certos para cada situação
    4. Subir de nível e se tornar um especialista
    
    ### 📊 Seu Progresso Atual:
    """)
    
    # Métricas do jogador
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📈 Nível", st.session_state.nivel)
    
    with col2:
        st.metric("⭐ XP Total", st.session_state.xp_total)
    
    with col3:
        st.metric("💰 Dinheiro", f"R$ {st.session_state.dinheiro}")
    
    with col4:
        st.metric("🏥 Reputação", f"{st.session_state.reputacao}/100")
    
    st.markdown("---")
    
    # Próximas missões disponíveis
    st.subheader("🎯 Próximas Missões Disponíveis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 🔬 **Medicina Nuclear**")
            st.markdown("**Calcular dose de I-131**")
            st.markdown("👤 Nível requerido: 1")
            st.markdown("⏱️ Duração: 10 min")
            if st.button("Iniciar Missão 1", key="missao1"):
                st.session_state.missao_atual = "farmacia_radioativa"
                st.rerun()
    
    with col2:
        with st.container(border=True):
            st.markdown("### 🏥 **Radioterapia**")
            st.markdown("**Calibrar acelerador**")
            st.markdown("👤 Nível requerido: 2")
            st.markdown("⏱️ Duração: 15 min")
            if st.button("Iniciar Missão 2", key="missao2"):
                st.session_state.missao_atual = "calibracao_acelerador"
                st.rerun()
    
    with col3:
        with st.container(border=True):
            st.markdown("### 🛡️ **Radioproteção**")
            st.markdown("**Encontrar fonte perdida**")
            st.markdown("👤 Nível requerido: 1")
            st.markdown("⏱️ Duração: 12 min")
            if st.button("Iniciar Missão 3", key="missao3"):
                st.session_state.missao_atual = "fonte_perdida"
                st.rerun()
    
    # Dicas do dia
    st.markdown("---")
    st.subheader("💡 Dica do Dia")
    
    dicas = [
        "💡 **Dica de Decaimento**: Use a fórmula A(t) = A₀ × (½)^(t/T) para calcular atividades remanescentes",
        "💡 **Dica de Detector**: Geiger satura acima de 5.000 cps - afaste-se de fontes fortes!",
        "💡 **Dica de Segurança**: Sempre use o princípio ALARA: tão baixo quanto razoavelmente alcançável",
        "💡 **Dica de Cálculo**: Verifique sempre as unidades antes de calcular!"
    ]
    
    st.info(random.choice(dicas))

# ============================================================
# MÓDULO 2: SISTEMA DE MISSÕES
# ============================================================

# ------------------------------------------------------------
# MISSÃO 1: FARMÁCIA RADIOATIVA
# ------------------------------------------------------------

def missao_farmacia_radioativa():
    """Missão: Calcular doses na farmácia de medicina nuclear"""
    
    st.title("🔬 MISSÃO: EMERGÊNCIA NA FARMÁCIA RADIOATIVA")
    
    # Contexto da missão
    st.markdown("""
    ### 📋 Contexto:
    **Hora:** 07:30 AM  
    **Local:** Farmácia Radioativa - Setor de Medicina Nuclear  
    
    A farmacêutica preparou doses de **Iodo-131** para pacientes com hipertireoidismo,
    mas calculou mal os tempos de decaimento. Agora os pacientes correm risco de
    receber doses incorretas!
    
    ### 🎯 Sua Missão:
    Calcular a atividade real de cada dose no horário marcado e decidir se pode
    ou não administrar.
    
    ### 📊 Dados do I-131:
    - Meia-vida: **8,04 dias**
    - Preparo inicial: todas às 06:00 AM
    - Atividade inicial: **3000 MBq** por dose
    """)
    
    st.markdown("---")
    
    # Pacientes para cálculo
    pacientes = [
        {"nome": "Paciente A - Dona Maria", "hora": "10:00", "dose_prescrita": 1850},
        {"nome": "Paciente B - Sr. João", "hora": "14:00", "dose_prescrita": 2400},
        {"nome": "Paciente C - Sra. Ana", "hora": "16:00", "dose_prescrita": 1500}
    ]
    
    st.subheader("📝 Cálculos Necessários")
    
    resultados = []
    todas_corretas = True
    
    for i, paciente in enumerate(pacientes):
        st.markdown(f"#### 👤 {paciente['nome']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            horas = st.number_input(
                f"Horas após preparo (06:00 → {paciente['hora']})",
                min_value=0.0,
                max_value=24.0,
                value=float(paciente['hora'].split(':')[0]) - 6,
                step=0.5,
                key=f"horas_{i}"
            )
            
            dose_prescrita = st.number_input(
                "Dose prescrita (MBq)",
                value=paciente['dose_prescrita'],
                key=f"dose_{i}"
            )
        
        with col2:
            if st.button(f"📊 Calcular Dose Real", key=f"calc_{i}"):
                # Cálculo do decaimento
                dias = horas / 24
                A_t = 3000 * (0.5) ** (dias / 8.04)
                
                # Percentual de diferença
                diferenca = ((A_t - dose_prescrita) / dose_prescrita) * 100
                
                # Exibir resultados
                st.metric("Atividade no horário", f"{A_t:.1f} MBq")
                st.metric("Diferença", f"{diferenca:.1f}%")
                
                # Verificar se está dentro dos limites
                limite_aceitavel = 5  # ±5%
                
                if abs(diferenca) <= limite_aceitavel:
                    st.success("✅ **DOSE ACEITÁVEL**")
                    st.info("Pode administrar com segurança")
                    resultado = True
                elif diferenca > 0:
                    st.error("❌ **DOSE EXCESSIVA**")
                    st.warning(f"**{diferenca:.1f}% acima** - Risco de hipotireoidismo!")
                    resultado = False
                    todas_corretas = False
                else:
                    st.error("❌ **DOSE INSUFICIENTE**")
                    st.warning(f"**{abs(diferenca):.1f}% abaixo** - Tratamento ineficaz!")
                    resultado = False
                    todas_corretas = False
                
                resultados.append(resultado)
                
                # Explicação teórica
                with st.expander("📚 Explicação Teórica"):
                    st.markdown(f"""
                    **Fórmula usada:** A(t) = A₀ × (½)^(t/T)
                    
                    **Cálculo:**
                    ```
                    A₀ = 3000 MBq
                    t = {horas} horas = {dias:.3f} dias
                    T = 8,04 dias
                    
                    t/T = {dias:.3f} / 8,04 = {dias/8.04:.4f}
                    (½)^({dias/8.04:.4f}) = {(0.5)**(dias/8.04):.4f}
                    
                    A(t) = 3000 × {(0.5)**(dias/8.04):.4f} = {A_t:.1f} MBq
                    ```
                    
                    **Limite clínico:** ±{limite_aceitavel}%
                    """)
    
    # Finalização da missão
    st.markdown("---")
    
    if st.button("🎯 Finalizar Missão", type="primary"):
        if len(resultados) == 3:
            acertos = sum(resultados)
            
            if todas_corretas:
                st.balloons()
                st.success("🎉 **MISSÃO COMPLETA COM ÊXITO!**")
                
                # Recompensas
                recompensa_xp = 150
                recompensa_dinheiro = 1000
                
                st.session_state.xp_total += recompensa_xp
                st.session_state.xp += recompensa_xp
                st.session_state.dinheiro += recompensa_dinheiro
                st.session_state.reputacao += 10
                st.session_state.missoes_completas += 1
                
                st.markdown(f"""
                ### 🏆 Recompensas:
                - ⭐ **+{recompensa_xp} XP**
                - 💰 **+R$ {recompensa_dinheiro}**
                - 🏥 **+10 Reputação**
                
                ### 📈 Progresso:
                - XP Total: **{st.session_state.xp_total}**
                - Reputação: **{st.session_state.reputacao}/100**
                """)
                
                # Verificar subida de nível
                if st.session_state.xp >= st.session_state.nivel * 100:
                    st.session_state.nivel += 1
                    st.session_state.xp = 0
                    st.success(f"🎊 **PARABÉNS! Você subiu para o nível {st.session_state.nivel}!**")
                
                # Marcar conquista
                if not st.session_state.conquistas['primeiro_calculo']:
                    st.session_state.conquistas['primeiro_calculo'] = True
                    st.info("🏅 **Conquista desbloqueada: Primeiro Cálculo!**")
                    
            else:
                st.error(f"⚠️ **MISSÃO INCOMPLETA** - {3 - acertos} cálculos incorretos")
                st.warning("Revise os cálculos e tente novamente!")
                st.session_state.erros_cometidos += 1
        else:
            st.warning("⏳ Complete todos os cálculos antes de finalizar!")

# ------------------------------------------------------------
# MISSÃO 2: CALIBRAÇÃO DE ACELERADOR
# ------------------------------------------------------------

def missao_calibracao_acelerador():
    """Missão: Calibrar acelerador linear para radioterapia"""
    
    st.title("🏥 MISSÃO: CALIBRAÇÃO DE ACELERADOR LINEAR")
    
    # Verificar nível mínimo
    if st.session_state.nivel < 2:
        st.error("🚫 **NÍVEL INSUFICIENTE**")
        st.warning("Você precisa estar no nível 2 para esta missão!")
        if st.button("Voltar ao Painel"):
            st.session_state.missao_atual = None
            st.rerun()
        return
    
    # Contexto da missão
    st.markdown("""
    ### 📋 Contexto:
    **Hora:** 08:00 AM  
    **Local:** Bunker de Radioterapia - Acelerador Linear Varian TrueBeam  
    
    O acelerador acabou de passar por manutenção e precisa ser recalibrado
    antes do primeiro paciente. Você é responsável pela dosimetria de referência.
    
    ### 🎯 Sua Missão:
    Usar a câmara de ionização para medir a taxa de dose e ajustar o acelerador
    para fornecer exatamente 2 Gy/min no isocentro.
    
    ### 🧪 Equipamento:
    - Câmara de Ionização Farmer 0,6 cm³
    - Eletrômetro de precisão
    - Fantoma de água
    """)
    
    st.markdown("---")
    
    # Simulação da medição
    st.subheader("🔬 Medição com Câmara de Ionização")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Parâmetros da Medição")
        
        corrente = st.number_input(
            "Corrente medida (A)",
            min_value=0.0,
            max_value=1e-6,
            value=4.2e-9,
            format="%.2e",
            help="Corrente elétrica gerada na câmara"
        )
        
        tempo = st.number_input(
            "Tempo de exposição (s)",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1
        )
        
        volume = st.number_input(
            "Volume da câmara (cm³)",
            min_value=0.01,
            max_value=10.0,
            value=0.6,
            step=0.1
        )
    
    with col2:
        st.markdown("### ⚙️ Constantes Físicas")
        
        W = st.number_input(
            "Energia por par íon-elétron (eV)",
            min_value=20.0,
            max_value=50.0,
            value=34.0,
            step=0.1,
            help="Valor para ar seco: 34 eV"
        )
        
        densidade_ar = st.number_input(
            "Densidade do ar (kg/m³)",
            min_value=1.0,
            max_value=1.5,
            value=1.2,
            step=0.1
        )
        
        fator_agua = st.number_input(
            "Fator ar→água",
            min_value=1.0,
            max_value=1.2,
            value=1.11,
            step=0.01,
            help="Para fótons de 6 MV: ~1,11"
        )
    
    # Cálculo da dose
    if st.button("📈 Calcular Dose"):
        st.markdown("---")
        st.subheader("🧮 Cálculos Passo a Passo")
        
        # Passo 1: Carga coletada
        Q = corrente * tempo
        st.markdown(f"**1. Carga coletada:** Q = I × t = {corrente:.2e} × {tempo} = {Q:.2e} C")
        
        # Passo 2: Número de pares
        e = 1.6e-19  # Carga do elétron
        N = Q / e
        st.markdown(f"**2. Pares íon-elétron:** N = Q/e = {Q:.2e} / 1,6×10⁻¹⁹ = {N:.2e}")
        
        # Passo 3: Energia absorvida
        E_eV = N * W
        E_J = E_eV * 1.6e-19
        st.markdown(f"**3. Energia absorvida:** E = N × W = {N:.2e} × {W} = {E_eV:.2e} eV = {E_J:.2e} J")
        
        # Passo 4: Massa de ar
        volume_m3 = volume * 1e-6
        m = densidade_ar * volume_m3
        st.markdown(f"**4. Massa de ar:** m = ρ × V = {densidade_ar} × {volume_m3:.2e} = {m:.2e} kg")
        
        # Passo 5: Dose no ar
        D_ar = E_J / m
        st.markdown(f"**5. Dose no ar:** D = E/m = {E_J:.2e} / {m:.2e} = {D_ar:.4f} Gy")
        
        # Passo 6: Dose em água
        D_agua = D_ar * fator_agua
        st.markdown(f"**6. Dose em água:** D_água = D_ar × fator = {D_ar:.4f} × {fator_agua} = {D_agua:.4f} Gy")
        
        # Passo 7: Taxa de dose
        taxa = D_agua / tempo * 60  # Gy/min
        st.markdown(f"**7. Taxa de dose:** Ṋ = D/t × 60 = {D_agua:.4f}/{tempo} × 60 = {taxa:.2f} Gy/min")
        
        # Verificação do objetivo
        st.markdown("---")
        st.subheader("🎯 Verificação da Calibração")
        
        objetivo = 2.0  # Gy/min
        diferenca = ((taxa - objetivo) / objetivo) * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Taxa medida", f"{taxa:.3f} Gy/min")
        
        with col2:
            st.metric("Objetivo", f"{objetivo} Gy/min")
        
        if abs(diferenca) <= 1.0:  # ±1% é excelente
            st.success(f"✅ **CALIBRAÇÃO PERFEITA!** Erro: {diferenca:.2f}%")
            st.balloons()
            
            # Recompensas
            recompensa_xp = 200
            recompensa_dinheiro = 1500
            
            st.session_state.xp_total += recompensa_xp
            st.session_state.xp += recompensa_xp
            st.session_state.dinheiro += recompensa_dinheiro
            st.session_state.reputacao += 15
            st.session_state.missoes_completas += 1
            
            st.markdown(f"""
            ### 🏆 Recompensas por calibração precisa:
            - ⭐ **+{recompensa_xp} XP**
            - 💰 **+R$ {recompensa_dinheiro}**
            - 🏥 **+15 Reputação**
            """)
            
        elif abs(diferenca) <= 3.0:  # ±3% é aceitável
            st.warning(f"⚠️ **CALIBRAÇÃO ACEITÁVEL** Erro: {diferenca:.2f}%")
            st.info("Na prática, seria aceito mas requer atenção")
            
            # Recompensas menores
            recompensa_xp = 100
            recompensa_dinheiro = 800
            
            st.session_state.xp_total += recompensa_xp
            st.session_state.xp += recompensa_xp
            st.session_state.dinheiro += recompensa_dinheiro
            st.session_state.reputacao += 5
            st.session_state.missoes_completas += 1
            
        else:
            st.error(f"❌ **CALIBRAÇÃO INACEITÁVEL!** Erro: {diferenca:.2f}%")
            st.warning("Ajuste os parâmetros e tente novamente!")
            st.session_state.erros_cometidos += 1

# ------------------------------------------------------------
# MISSÃO 3: FONTE PERDIDA
# ------------------------------------------------------------

def missao_fonte_perdida():
    """Missão: Encontrar fonte radioativa perdida no laboratório"""
    
    st.title("🕵️ MISSÃO: DETETIVE RADIOATIVO")
    
    # Inicializar posição da fonte se não existir
    if 'fonte_pos' not in st.session_state:
        st.session_state.fonte_pos = {
            'x': random.randint(0, 9),
            'y': random.randint(0, 9)
        }
        st.session_state.tentativas = 0
        st.session_state.dicas_usadas = 0
        st.session_state.detector_atual = "geiger"
    
    # Contexto da missão
    st.markdown("""
    ### 📋 Contexto:
    **Hora:** 22:30 PM  
    **Local:** Laboratório de Física Médica  
    
    Uma fonte de **Cs-137** (450 MBq) desapareceu do cofre blindado.
    A fonte é perigosa e precisa ser encontrada urgentemente!
    
    ### 🎯 Sua Missão:
    Usar diferentes detectores para localizar a fonte no laboratório.
    
    ### ⚠️ Limitações:
    - Geiger satura perto da fonte
    - Câmara de ionização precisa de calibração
    - NaI tem melhor sensibilidade mas é mais lento
    """)
    
    st.markdown("---")
    
    # Mapa do laboratório
    st.subheader("🗺️ Mapa do Laboratório (10×10 metros)")
    
    # Criar mapa interativo
    mapa_html = """
    <style>
    .mapa {
        display: grid;
        grid-template-columns: repeat(10, 40px);
        grid-template-rows: repeat(10, 40px);
        gap: 2px;
        margin: 20px auto;
        width: fit-content;
    }
    .celula {
        width: 40px;
        height: 40px;
        border: 1px solid #ccc;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #f8f9fa;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .celula:hover {
        background-color: #e9ecef;
    }
    .selecionada {
        background-color: #4CAF50 !important;
        color: white;
    }
    .fonte {
        background-color: #FF5252 !important;
        color: white;
    }
    </style>
    
    <div class="mapa">
    """
    
    # Gerar células do mapa
    for y in range(10):
        for x in range(10):
            celula_class = "celula"
            if 'pos_selecionada' in st.session_state:
                if st.session_state.pos_selecionada == (x, y):
                    celula_class += " selecionada"
            if st.session_state.fonte_pos == {'x': x, 'y': y}:
                celula_class += " fonte"
            
            mapa_html += f'<div class="{celula_class}" data-x="{x}" data-y="{y}">({x},{y})</div>'
    
    mapa_html += "</div>"
    
    st.components.v1.html(mapa_html, height=450)
    
    # Controles de interação
    st.markdown("---")
    st.subheader("🔧 Controles de Busca")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📍 Escolher Posição")
        pos_x = st.slider("Coordenada X", 0, 9, 5)
        pos_y = st.slider("Coordenada Y", 0, 9, 5)
        
        if st.button("🎯 Ir para esta posição"):
            st.session_state.pos_selecionada = (pos_x, pos_y)
            st.session_state.tentativas += 1
            st.rerun()
    
    with col2:
        st.markdown("### 🔍 Escolher Detector")
        
        detector = st.radio(
            "Selecione o detector:",
            ["Geiger-Müller", "Câmara de Ionização", "Detector NaI(Tl)"],
            key="detector_radio"
        )
        
        st.session_state.detector_atual = detector
        
        if st.button("📡 Realizar Medição", type="primary"):
            # Calcular distância até a fonte
            distancia = np.sqrt((pos_x - st.session_state.fonte_pos['x'])**2 + 
                              (pos_y - st.session_state.fonte_pos['y'])**2)
            
            st.markdown("---")
            st.subheader("📊 Resultado da Medição")
            
            # Resultados baseados no detector e distância
            if detector == "Geiger-Müller":
                if distancia < 1:
                    st.error("⚠️ **SATURAÇÃO COMPLETA!**")
                    st.warning("O Geiger não consegue medir - taxa muito alta!")
                    taxa = "> 50.000 cps (saturado)"
                elif distancia < 3:
                    st.success("📈 **SINAL FORTE**")
                    taxa = f"~{int(10000/(distancia+1))} cps"
                elif distancia < 6:
                    st.info("📉 **SINAL MODERADO**")
                    taxa = f"~{int(1000/(distancia+1))} cps"
                else:
                    st.warning("🔇 **SINAL FRACO**")
                    taxa = f"< 100 cps"
                
                st.metric("Taxa de contagem", taxa)
                
            elif detector == "Câmara de Ionização":
                # Calcular corrente aproximada
                corrente = 450e6 / (4 * np.pi * (distancia+0.1)**2) * 1.6e-19 * 100
                st.metric("Corrente medida", f"{corrente:.2e} A")
                
                if distancia < 2:
                    st.success("🔋 **CORRENTE ALTA** - Fonte próxima!")
                elif distancia < 5:
                    st.info("⚡ **CORRENTE MODERADA**")
                else:
                    st.warning("🔌 **CORRENTE BAIXA**")
                    
            elif detector == "Detector NaI(Tl)":
                # Simular espectro
                st.success("📊 **ESPECTRO OBTIDO**")
                
                # Criar gráfico do espectro simulado
                fig, ax = plt.subplots(figsize=(10, 4))
                
                # Pico principal do Cs-137
                energia = np.linspace(0, 800, 400)
                pico_principal = 300 * np.exp(-(energia - 662)**2 / (2 * 30**2))
                
                # Ruído de fundo
                ruido = 20 * np.exp(-energia / 200)
                
                espectro = pico_principal + ruido + np.random.normal(0, 5, len(energia))
                
                ax.plot(energia, espectro, 'b-', linewidth=1.5)
                ax.axvline(x=662, color='r', linestyle='--', alpha=0.7, label='662 keV (Cs-137)')
                ax.fill_between(energia, 0, espectro, alpha=0.3)
                
                ax.set_xlabel('Energia (keV)')
                ax.set_ylabel('Contagens (u.a.)')
                ax.set_title('Espectro Simulado - Detector NaI(Tl)')
                ax.legend()
                ax.grid(True, alpha=0.3)
                
                st.pyplot(fig)
            
            # Dica baseada na distância
            st.markdown("---")
            st.subheader("💡 Dica do Sistema")
            
            if distancia < 1:
                st.success("🎯 **VOCÊ ENCONTROU A FONTE!**")
                st.balloons()
                
                # Recompensas
                recompensa_xp = 180
                recompensa_dinheiro = 1200
                
                st.session_state.xp_total += recompensa_xp
                st.session_state.xp += recompensa_xp
                st.session_state.dinheiro += recompensa_dinheiro
                st.session_state.reputacao += 12
                st.session_state.missoes_completas += 1
                
                # Marcar conquista
                if st.session_state.tentativas < 5:
                    if not st.session_state.conquistas['detetive_perfeito']:
                        st.session_state.conquistas['detetive_perfeito'] = True
                        st.info("🏅 **Conquista: Detetive Perfeito!**")
                
                st.markdown(f"""
                ### 🏆 Missão Cumprida!
                - ⭐ **+{recompensa_xp} XP**
                - 💰 **+R$ {recompensa_dinheiro}**
                - 🏥 **+12 Reputação**
                - 🔍 **Tentativas:** {st.session_state.tentativas}
                """)
                
                # Resetar posição da fonte
                del st.session_state.fonte_pos
                
            elif distancia < 2:
                st.success("🔥 **MUITO QUENTE!** Quase encontrou!")
            elif distancia < 4:
                st.info("🌡️ **QUENTE** - Continue nesta direção")
            elif distancia < 7:
                st.warning("🌤️ **MORNO** - Você está no caminho certo")
            else:
                st.error("❄️ **FRIO** - Tente outra área do laboratório")
    
    # Botão de ajuda
    if st.button("🆘 Usar Dica (custa 50 de reputação)"):
        if st.session_state.reputacao >= 50:
            st.session_state.reputacao -= 50
            st.session_state.dicas_usadas += 1
            
            # Dar dica sobre a posição
            fonte_x = st.session_state.fonte_pos['x']
            fonte_y = st.session_state.fonte_pos['y']
            
            dicas = [
                f"A fonte está na linha {fonte_x} do mapa",
                f"A fonte está na coluna {fonte_y} do mapa",
                f"A fonte está no quadrante {fonte_x//3 + 1}{fonte_y//3 + 1}",
                f"Distância da origem: √({fonte_x}² + {fonte_y}²) ≈ {np.sqrt(fonte_x**2 + fonte_y**2):.1f}"
            ]
            
            st.info(f"💡 **Dica {st.session_state.dicas_usadas}:** {random.choice(dicas)}")
        else:
            st.warning("Reputação insuficiente para dicas!")

# ============================================================
# MÓDULO 3: CALCULADORAS INTERATIVAS
# ============================================================

def mostrar_calculadoras():
    """Módulo com calculadoras interativas"""
    
    st.title("🧮 CALCULADORAS RADIOLÓGICAS")
    
    calculadora = st.selectbox(
        "Selecione a calculadora:",
        ["📉 Decaimento Radioativo", "⚡ Efeito Fotoelétrico", 
         "🔄 Efeito Compton", "📊 Dose com Câmara de Ionização"]
    )
    
    if calculadora == "📉 Decaimento Radioativo":
        calculadora_decaimento()
    elif calculadora == "⚡ Efeito Fotoelétrico":
        calculadora_fotoeletrico()
    elif calculadora == "🔄 Efeito Compton":
        calculadora_compton()
    elif calculadora == "📊 Dose com Câmara de Ionização":
        calculadora_dose()

def calculadora_decaimento():
    """Calculadora de decaimento radioativo"""
    
    st.subheader("📉 Calculadora de Decaimento Radioativo")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        A0 = st.number_input("Atividade Inicial (MBq)", 
                           min_value=0.0, value=1000.0, step=100.0)
    
    with col2:
        T_half = st.number_input("Meia-vida", 
                               min_value=0.0, value=6.01, step=0.1)
        T_unit = st.selectbox("Unidade tempo", ["horas", "dias", "anos"])
    
    with col3:
        t = st.number_input("Tempo decorrido", 
                          min_value=0.0, value=4.0, step=0.5)
        t_unit = st.selectbox("Unidade", ["horas", "dias", "anos"])
    
    # Converter para mesma unidade (simplificado)
    if T_unit != t_unit:
        st.warning("⚠️ Converta para a mesma unidade antes de calcular!")
    
    if st.button("Calcular Atividade Atual", type="primary"):
        A_t = A0 * (0.5) ** (t / T_half)
        
        st.success(f"**Atividade atual:** {A_t:.2f} MBq")
        
        # Gráfico
        fig, ax = plt.subplots(figsize=(10, 5))
        
        tempos = np.linspace(0, T_half * 3, 100)
        atividades = A0 * (0.5) ** (tempos / T_half)
        
        ax.plot(tempos, atividades, 'b-', linewidth=2, label='Decaimento')
        ax.axvline(x=t, color='r', linestyle='--', alpha=0.7, 
                  label=f'Tempo atual ({t} {t_unit})')
        ax.axhline(y=A_t, color='g', linestyle='--', alpha=0.7,
                  label=f'Atividade: {A_t:.1f} MBq')
        
        ax.set_xlabel(f'Tempo ({t_unit})')
        ax.set_ylabel('Atividade (MBq)')
        ax.set_title('Curva de Decaimento Radioativo')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        
        # Explicação
        with st.expander("📚 Explicação Detalhada"):
            st.markdown(f"""
            **Fórmula:** A(t) = A₀ × (½)^(t/T₁/₂)
            
            **Cálculo passo a passo:**
            1. A₀ = {A0} MBq
            2. t/T₁/₂ = {t} / {T_half} = {t/T_half:.4f}
            3. (½)^({t/T_half:.4f}) = {0.5**(t/T_half):.4f}
            4. A(t) = {A0} × {0.5**(t/T_half):.4f} = **{A_t:.2f} MBq**
            
            **Interpretação:**
            - Após {t} {t_unit}, a atividade caiu para {A_t/A0*100:.1f}% do valor inicial
            - Em {T_half} {T_unit} (1 meia-vida), será {A0/2:.1f} MBq
            - Em {T_half*2} {T_unit} (2 meias-vidas), será {A0/4:.1f} MBq
            """)

def calculadora_fotoeletrico():
    """Calculadora do efeito fotoelétrico"""
    
    st.subheader("⚡ Calculadora do Efeito Fotoelétrico")
    
    st.markdown("""
    **Fórmula:** E_cinética = E_fóton - E_ligação
    
    Onde:
    - E_cinética: energia do elétron ejetado
    - E_fóton: energia do fóton incidente  
    - E_ligação: energia necessária para remover o elétron
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        E_foton = st.number_input("Energia do fóton (keV)", 
                                min_value=1.0, value=80.0, step=1.0)
    
    with col2:
        E_ligacao = st.number_input("Energia de ligação (keV)", 
                                  min_value=0.0, value=69.5, step=0.1)
    
    if st.button("Calcular Energia Cinética"):
        if E_foton < E_ligacao:
            st.error("❌ **Energia insuficiente!**")
            st.warning(f"O fóton precisa de pelo menos {E_ligacao} keV para ejetar o elétron")
        else:
            E_cinetica = E_foton - E_ligacao
            st.success(f"**Energia cinética do elétron:** {E_cinetica:.2f} keV")
            
            # Informações adicionais
            with st.expander("📚 Informações Adicionais"):
                st.markdown(f"""
                **Processo físico:**
                1. Fóton de {E_foton} keV é absorvido pelo átomo
                2. {E_ligacao} keV são usados para vencer a força de ligação
                3. Os {E_cinetica:.2f} keV restantes são transformados em energia cinética
                
                **Aplicações práticas:**
                - **Radiografia:** Contraste entre ossos e tecidos moles
                - **Blindagem:** Chumbo é eficaz devido ao alto Z (Z=82)
                - **Detectores:** Base para detectores de raios-X
                
                **Fato importante:** 
                Probabilidade do efeito fotoelétrico ∝ Z⁴/E³
                Ou seja: aumenta muito com Z alto e energia baixa
                """)

def calculadora_compton():
    """Calculadora do efeito Compton"""
    
    st.subheader("🔄 Calculadora do Efeito Compton")
    
    st.markdown("""
    **Fórmula:** E' = E / [1 + (E/511)(1 - cosθ)]
    
    Onde:
    - E: energia do fóton incidente (keV)
    - E': energia do fóton espalhado (keV)
    - θ: ângulo de espalhamento (graus)
    - 511 keV: energia de repouso do elétron
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        E = st.number_input("Energia incidente E (keV)", 
                          min_value=10.0, value=150.0, step=10.0)
    
    with col2:
        theta = st.slider("Ângulo de espalhamento θ (graus)", 
                         min_value=0, max_value=180, value=90)
    
    if st.button("Calcular Energia Espalhada"):
        theta_rad = np.radians(theta)
        
        # Fórmula do Compton
        E_linha = E / (1 + (E/511) * (1 - np.cos(theta_rad)))
        
        # Energia do elétron de recuo
        E_eletron = E - E_linha
        
        st.success(f"**Energia do fóton espalhado:** {E_linha:.2f} keV")
        st.info(f"**Energia do elétron de recuo:** {E_eletron:.2f} keV")
        
        # Gráfico da variação com o ângulo
        fig, ax = plt.subplots(figsize=(10, 5))
        
        angulos = np.linspace(0, 180, 181)
        energias = E / (1 + (E/511) * (1 - np.cos(np.radians(angulos))))
        
        ax.plot(angulos, energias, 'b-', linewidth=2)
        ax.scatter([theta], [E_linha], color='red', s=100, zorder=5,
                  label=f'θ={theta}°, E\'={E_linha:.1f} keV')
        
        ax.set_xlabel('Ângulo de Espalhamento θ (graus)')
        ax.set_ylabel('Energia do Fóton Espalhado E\' (keV)')
        ax.set_title(f'Variação de E\' com θ para E={E} keV')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        
        # Explicação
        with st.expander("📚 Explicação Detalhada"):
            st.markdown(f"""
            **Cálculo para θ = {theta}°:**
            1. E = {E} keV
            2. cos({theta}°) = {np.cos(theta_rad):.4f}
            3. (E/511) = {E}/511 = {E/511:.4f}
            4. 1 - cosθ = 1 - {np.cos(theta_rad):.4f} = {1-np.cos(theta_rad):.4f}
            5. (E/511)(1-cosθ) = {E/511:.4f} × {1-np.cos(theta_rad):.4f} = {(E/511)*(1-np.cos(theta_rad)):.4f}
            6. E' = {E} / [1 + {(E/511)*(1-np.cos(theta_rad)):.4f}] = **{E_linha:.2f} keV**
            
            **Características do efeito Compton:**
            - Domina na faixa de **30 keV a 1 MeV**
            - Independente do número atômico Z
            - Principal fonte de **radiação espalhada** em diagnóstico
            - Reduz o contraste na imagem radiográfica
            
            **Aplicações:**
            - **Tomografia:** Requer correção do espalhamento
            - **Proteção:** Principal fonte de dose ocupacional
            - **Espalhamento Compton:** Técnica de imageamento
            """)

def calculadora_dose():
    """Calculadora de dose com câmara de ionização"""
    
    st.subheader("📊 Calculadora de Dose com Câmara de Ionização")
    
    st.markdown("""
    **Fórmulas:**
    1. Q = I × t
    2. N = Q / e
    3. E = N × W
    4. Dose = E / m
    """)
    
    # Entrada de parâmetros
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Parâmetros de Medição")
        I = st.number_input("Corrente (A)", value=4.2e-9, format="%.2e")
        t = st.number_input("Tempo (s)", value=1.0, step=0.1)
        volume = st.number_input("Volume da câmara (cm³)", value=0.6, step=0.1)
    
    with col2:
        st.markdown("### ⚙️ Constantes Físicas")
        W = st.number_input("W (eV/par)", value=34.0, step=0.1)
        densidade = st.number_input("Densidade do ar (kg/m³)", value=1.2, step=0.1)
        fator = st.number_input("Fator ar→água", value=1.11, step=0.01)
    
    if st.button("Calcular Dose", type="primary"):
        # Cálculos passo a passo
        st.markdown("---")
        st.subheader("🧮 Cálculos Passo a Passo")
        
        calculos = []
        
        # 1. Carga
        Q = I * t
        calculos.append(f"**1. Carga coletada:** Q = I × t = {I:.2e} × {t} = {Q:.2e} C")
        
        # 2. Pares
        e = 1.6e-19
        N = Q / e
        calculos.append(f"**2. Pares íon-elétron:** N = Q/e = {Q:.2e} / 1,6×10⁻¹⁹ = {N:.2e}")
        
        # 3. Energia
        E_eV = N * W
        E_J = E_eV * 1.6e-19
        calculos.append(f"**3. Energia absorvida:** E = N × W = {N:.2e} × {W} = {E_eV:.2e} eV = {E_J:.2e} J")
        
        # 4. Massa
        volume_m3 = volume * 1e-6
        m = densidade * volume_m3
        calculos.append(f"**4. Massa de ar:** m = ρ × V = {densidade} × {volume_m3:.2e} = {m:.2e} kg")
        
        # 5. Dose no ar
        D_ar = E_J / m
        calculos.append(f"**5. Dose no ar:** D_ar = E/m = {E_J:.2e} / {m:.2e} = {D_ar:.4f} Gy")
        
        # 6. Dose em água
        D_agua = D_ar * fator
        calculos.append(f"**6. Dose em água:** D_água = D_ar × fator = {D_ar:.4f} × {fator} = {D_agua:.4f} Gy")
        
        # 7. Taxa de dose
        taxa = D_agua / t
        calculos.append(f"**7. Taxa de dose:** Ṋ = D_água/t = {D_agua:.4f} / {t} = {taxa:.4f} Gy/s = {taxa*60:.2f} Gy/min")
        
        # Mostrar todos os cálculos
        for calc in calculos:
            st.markdown(calc)
        
        # Resumo
        st.markdown("---")
        st.subheader("📋 Resumo dos Resultados")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Dose no ar", f"{D_ar:.4f} Gy")
        
        with col2:
            st.metric("Dose em água", f"{D_agua:.4f} Gy")
        
        with col3:
            st.metric("Taxa de dose", f"{taxa*60:.2f} Gy/min")

# ============================================================
# MÓDULO 4: SIMULADORES
# ============================================================

def mostrar_simuladores():
    """Módulo com simuladores interativos"""
    
    st.title("🔬 SIMULADORES DE DETECTORES")
    
    simulador = st.selectbox(
        "Selecione o simulador:",
        ["📡 Simulador de Detectores", "🌡️ Simulador de Decaimento", 
         "🛡️ Simulador de Blindagem"]
    )
    
    if simulador == "📡 Simulador de Detectores":
        simulador_detectores()
    elif simulador == "🌡️ Simulador de Decaimento":
        simulador_decaimento()
    elif simulador == "🛡️ Simulador de Blindagem":
        simulador_blindagem()

def simulador_detectores():
    """Simulador comparativo de detectores"""
    
    st.subheader("📡 Simulador Comparativo de Detectores")
    
    # Seleção de parâmetros
    col1, col2 = st.columns(2)
    
    with col1:
        fonte = st.selectbox(
            "Fonte radioativa",
            ["Cs-137 (662 keV)", "Co-60 (1.25 MeV)", "I-131 (364 keV)", 
             "Tc-99m (140 keV)", "Am-241 (59.5 keV)"]
        )
        
        # Mapear para energias
        energias = {
            "Cs-137 (662 keV)": 662,
            "Co-60 (1.25 MeV)": 1250,
            "I-131 (364 keV)": 364,
            "Tc-99m (140 keV)": 140,
            "Am-241 (59.5 keV)": 59.5
        }
        
        E = energias[fonte]
    
    with col2:
        atividade = st.number_input("Atividade (MBq)", value=100.0, step=10.0)
        distancia = st.slider("Distância (m)", 0.1, 10.0, 1.0, 0.1)
    
    # Parâmetros dos detectores
    detectores = {
        "Geiger-Müller": {
            "eficiencia": 0.01,
            "resolucao": "N/A",
            "tempo_morto": 200,
            "custo": 500,
            "aplicacao": "Monitoração presença"
        },
        "Câmara de Ionização": {
            "eficiencia": 0.05,
            "resolucao": "N/A",
            "tempo_morto": 0,
            "custo": 2000,
            "aplicacao": "Dosimetria absoluta"
        },
        "Detector Proporcional": {
            "eficiencia": 0.08,
            "resolucao": "10-20%",
            "tempo_morto": 1,
            "custo": 3000,
            "aplicacao": "Espectrometria α/β"
        },
        "NaI(Tl)": {
            "eficiencia": 0.25,
            "resolucao": "6-8%",
            "tempo_morto": 0.1,
            "custo": 5000,
            "aplicacao": "Medicina nuclear"
        }
    }
    
    if st.button("Simular Todos os Detectores"):
        st.markdown("---")
        st.subheader("📊 Resultados da Simulação")
        
        # Calcular fator geométrico
        area_detector = 0.01  # m² (aproximado)
        area_esfera = 4 * np.pi * distancia**2
        fator_geometrico = area_detector / area_esfera
        
        # Taxa de emissão
        taxa_emissao = atividade * 1e6  # Bq
        
        resultados = []
        
        for nome, params in detectores.items():
            # Taxa detectada
            taxa_detectada = taxa_emissao * fator_geometrico * params["eficiencia"]
            
            # Verificar saturação para Geiger
            if nome == "Geiger-Müller" and taxa_detectada > 5000:
                status = "🔴 SATURADO"
                taxa_display = "> 5.000 cps (saturado)"
            else:
                status = "🟢 OPERANDO"
                taxa_display = f"{taxa_detectada:,.0f} cps"
            
            resultados.append({
                "Detector": nome,
                "Eficiência": f"{params['eficiencia']*100:.1f}%",
                "Resolução": params["resolucao"],
                "Taxa": taxa_display,
                "Status": status,
                "Aplicação": params["aplicacao"],
                "Custo": f"R$ {params['custo']}"
            })
        
        # Exibir tabela
        df = pd.DataFrame(resultados)
        st.dataframe(df, use_container_width=True)
        
        # Gráfico comparativo
        fig, ax = plt.subplots(figsize=(10, 5))
        
        nomes = [r["Detector"] for r in resultados]
        taxas = []
        for r in resultados:
            if "saturado" in r["Taxa"]:
                taxas.append(6000)  # Valor para saturação
            else:
                taxas.append(float(r["Taxa"].replace(" cps", "").replace(",", "")))
        
        bars = ax.bar(nomes, taxas, color=['red' if t == 6000 else 'blue' for t in taxas])
        ax.axhline(y=5000, color='orange', linestyle='--', label='Limite Geiger (5.000 cps)')
        
        ax.set_ylabel('Taxa de Contagem (cps)')
        ax.set_title('Comparação de Detectores')
        ax.legend()
        ax.grid(True, axis='y', alpha=0.3)
        
        # Adicionar valores nas barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 50,
                   f'{height:,.0f}', ha='center', va='bottom', fontsize=9)
        
        st.pyplot(fig)
        
        # Conclusões
        st.markdown("---")
        st.subheader("💡 Conclusões da Simulação")
        
        with st.expander("📚 Análise Detalhada"):
            st.markdown(f"""
            **Para fonte de {fonte} ({E} keV) a {distancia} m:**
            
            1. **Geiger-Müller:** {'**Satura!** Use outro detector ou aumente a distância.' if taxas[0] == 6000 else 'Adequado para monitoração.'}
            
            2. **Câmara de Ionização:** {'Corrente muito baixa para esta distância.' if taxas[1] < 100 else 'Ideal para dosimetria precisa.'}
            
            3. **Detector Proporcional:** Boa para espectrometria nesta faixa de energia.
            
            4. **NaI(Tl):** Excelente eficiência, ideal para quantificação.
            
            **Recomendação:** {recomendar_detector(E, atividade, distancia)}
            """)

def recomendar_detector(energia, atividade, distancia):
    """Recomenda o detector ideal baseado nos parâmetros"""
    
    if energia < 100:  # Baixa energia
        if atividade < 10:  # Baixa atividade
            return "**Câmara de Ionização** para dosimetria precisa"
        else:
            return "**NaI(Tl)** para melhor eficiência"
    
    elif energia < 500:  # Energia média
        if distancia < 2:  # Perto
            return "**Detector Proporcional** (Geiger pode saturar)"
        else:
            return "**NaI(Tl)** ou **Geiger** para monitoração"
    
    else:  # Alta energia
        return "**NaI(Tl)** para melhor eficiência em gama"

def simulador_decaimento():
    """Simulador de decaimento de múltiplos radionuclídeos"""
    
    st.subheader("🌡️ Simulador de Decaimento de Radionuclídeos")
    
    # Seleção de radionuclídeos
    radionuclideos = {
        "Tc-99m": {"T": 6.01, "unidade": "horas", "usos": "Cintilografia"},
        "I-131": {"T": 8.04, "unidade": "dias", "usos": "Terapia tireoide"},
        "F-18": {"T": 109.7, "unidade": "minutos", "usos": "PET"},
        "Co-60": {"T": 5.27, "unidade": "anos", "usos": "Radioterapia"},
        "Cs-137": {"T": 30.17, "unidade": "anos", "usos": "Calibração"}
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        selecionados = st.multiselect(
            "Selecione os radionuclídeos para comparar:",
            list(radionuclideos.keys()),
            default=["Tc-99m", "I-131", "F-18"]
        )
        
        A0 = st.number_input("Atividade inicial (MBq)", value=1000.0)
    
    with col2:
        tempo = st.number_input("Tempo decorrido", value=24.0)
        tempo_unidade = st.selectbox("Unidade de tempo", ["horas", "dias", "anos"])
    
    if st.button("Simular Decaimento"):
        if not selecionados:
            st.warning("Selecione pelo menos um radionuclídeo!")
            return
        
        st.markdown("---")
        
        # Criar gráfico
        fig, ax = plt.subplots(figsize=(12, 6))
        
        cores = plt.cm.tab10(np.linspace(0, 1, len(selecionados)))
        
        for i, nuclideo in enumerate(selecionados):
            params = radionuclideos[nuclideo]
            T = params["T"]
            
            # Converter para horas para padronizar
            if params["unidade"] == "dias":
                T_horas = T * 24
            elif params["unidade"] == "anos":
                T_horas = T * 365 * 24
            elif params["unidade"] == "minutos":
                T_horas = T / 60
            else:  # horas
                T_horas = T
            
            # Tempo em horas
            if tempo_unidade == "dias":
                t_horas = tempo * 24
            elif tempo_unidade == "anos":
                t_horas = tempo * 365 * 24
            else:  # horas
                t_horas = tempo
            
            # Curva de decaimento
            tempos = np.linspace(0, min(T_horas * 5, 500), 500)
            atividades = A0 * (0.5) ** (tempos / T_horas)
            
            # Atividade no tempo especificado
            A_t = A0 * (0.5) ** (t_horas / T_horas)
            
            ax.plot(tempos, atividades, color=cores[i], linewidth=2, 
                   label=f"{nuclideo} (T₁/₂={T} {params['unidade']})")
            ax.scatter([t_horas], [A_t], color=cores[i], s=100, zorder=5)
            
            # Anotação
            ax.annotate(f'{A_t:.0f} MBq', 
                       xy=(t_horas, A_t),
                       xytext=(10, 10),
                       textcoords='offset points',
                       color=cores[i],
                       fontsize=9)
        
        ax.axvline(x=t_horas, color='gray', linestyle='--', alpha=0.5)
        ax.axhline(y=A0/2, color='gray', linestyle=':', alpha=0.5, label='50% atividade')
        ax.axhline(y=A0/4, color='gray', linestyle=':', alpha=0.3, label='25% atividade')
        
        ax.set_xlabel('Tempo (horas)')
        ax.set_ylabel('Atividade (MBq)')
        ax.set_title(f'Comparação de Decaimento Radionuclídeo\n(A₀ = {A0} MBq, t = {tempo} {tempo_unidade})')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(bottom=0)
        
        st.pyplot(fig)
        
        # Tabela de resultados
        st.markdown("---")
        st.subheader("📋 Resultados Numéricos")
        
        dados = []
        for nuclideo in selecionados:
            params = radionuclideos[nuclideo]
            T = params["T"]
            
            # Converter para unidade do tempo de entrada
            if params["unidade"] == tempo_unidade:
                A_t = A0 * (0.5) ** (tempo / T)
                percentual = A_t / A0 * 100
            else:
                # Conversão simplificada
                st.warning(f"Conversão entre {params['unidade']} e {tempo_unidade} é aproximada!")
                A_t = A0 * (0.5) ** (tempo / T)  # Aproximação
                percentual = A_t / A0 * 100
            
            dados.append({
                "Radionuclídeo": nuclideo,
                "Meia-vida": f"{T} {params['unidade']}",
                "Uso Principal": params["usos"],
                f"Atividade após {tempo} {tempo_unidade}": f"{A_t:.1f} MBq",
                "Percentual": f"{percentual:.1f}%"
            })
        
        df = pd.DataFrame(dados)
        st.dataframe(df, use_container_width=True)

def simulador_blindagem():
    """Simulador de blindagem radiológica"""
    
    st.subheader("🛡️ Simulador de Blindagem Radiológica")
    
    st.markdown("""
    **Fórmula da atenuação:** I = I₀ × e^(-μx)
    
    Onde:
    - I₀: intensidade inicial
    - I: intensidade transmitida  
    - μ: coeficiente de atenuação linear (cm⁻¹)
    - x: espessura do material (cm)
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        energia = st.selectbox(
            "Energia do fóton",
            ["50 keV (Raio-X diagnóstico)", "140 keV (Tc-99m)",
             "662 keV (Cs-137)", "1.25 MeV (Co-60)", "6 MeV (LINAC)"]
        )
        
        # Mapear energias
        energias_keV = {
            "50 keV (Raio-X diagnóstico)": 50,
            "140 keV (Tc-99m)": 140,
            "662 keV (Cs-137)": 662,
            "1.25 MeV (Co-60)": 1250,
            "6 MeV (LINAC)": 6000
        }
        
        E = energias_keV[energia]
        
        reducao_desejada = st.selectbox(
            "Redução desejada",
            ["10× (1 ordem)", "100× (2 ordens)", "1000× (3 ordens)", "10.000× (4 ordens)"]
        )
        
        reducoes = {
            "10× (1 ordem)": 10,
            "100× (2 ordens)": 100,
            "1000× (3 ordens)": 1000,
            "10.000× (4 ordens)": 10000
        }
        
        R = reducoes[reducao_desejada]
    
    with col2:
        material = st.selectbox(
            "Material de blindagem",
            ["Chumbo (Pb)", "Concreto", "Aço", "Água", "Tungstênio"]
        )
        
        # Coeficientes de atenuação aproximados (cm⁻¹)
        coeficientes = {
            "Chumbo (Pb)": {50: 85, 140: 2.5, 662: 1.2, 1250: 0.7, 6000: 0.5},
            "Concreto": {50: 2.0, 140: 0.3, 662: 0.15, 1250: 0.1, 6000: 0.05},
            "Aço": {50: 15, 140: 0.8, 662: 0.4, 1250: 0.25, 6000: 0.15},
            "Água": {50: 0.2, 140: 0.15, 662: 0.09, 1250: 0.06, 6000: 0.04},
            "Tungstênio": {50: 100, 140: 4.0, 662: 1.5, 1250: 0.9, 6000: 0.6}
        }
        
        # Interpolar se necessário
        mu = coeficientes[material].get(E)
        if mu is None:
            # Interpolação linear simples
            energias_conhecidas = list(coeficientes[material].keys())
            mus_conhecidos = [coeficientes[material][e] for e in energias_conhecidas]
            mu = np.interp(E, energias_conhecidas, mus_conhecidos)
    
    if st.button("Calcular Blindagem"):
        # Calcular espessura necessária
        # I/I₀ = 1/R = e^(-μx) → x = -ln(1/R) / μ
        x = -np.log(1/R) / mu
        
        st.success(f"**Espessura necessária de {material}:** {x:.2f} cm")
        
        # Gráfico da atenuação
        fig, ax = plt.subplots(figsize=(10, 5))
        
        espessuras = np.linspace(0, x * 2, 100)
        atenuacoes = np.exp(-mu * espessuras)
        
        ax.plot(espessuras, atenuacoes, 'b-', linewidth=2)
        ax.axvline(x=x, color='r', linestyle='--', alpha=0.7,
                  label=f'Espessura necessária: {x:.2f} cm')
        ax.axhline(y=1/R, color='g', linestyle='--', alpha=0.7,
                  label=f'Redução desejada: 1/{R}')
        
        ax.set_xlabel(f'Espessura de {material} (cm)')
        ax.set_ylabel('Transmissão (I/I₀)')
        ax.set_title(f'Atenuação de {E} keV em {material}\n(μ = {mu:.3f} cm⁻¹)')
        ax.set_yscale('log')
        ax.legend()
        ax.grid(True, alpha=0.3, which='both')
        
        st.pyplot(fig)
        
        # Informações adicionais
        with st.expander("📚 Informações Técnicas"):
            st.markdown(f"""
            **Cálculo detalhado:**
            1. Redução desejada: **1/{R}** da intensidade original
            2. Coeficiente de atenuação (μ): **{mu:.3f} cm⁻¹**
            3. Espessura: x = -ln(1/{R}) / {mu:.3f} = **{x:.2f} cm**
            
            **Comparação com outros materiais:**
            """)
            
            # Comparar com outros materiais
            comparacao = []
            for mat in coeficientes.keys():
                if mat != material:
                    mu_outro = coeficientes[mat].get(E)
                    if mu_outro:
                        x_outro = -np.log(1/R) / mu_outro
                        comparacao.append({
                            "Material": mat,
                            "μ (cm⁻¹)": f"{mu_outro:.3f}",
                            "Espessura necessária (cm)": f"{x_outro:.1f}",
                            "Relação": f"{x_outro/x:.1f}×"
                        })
            
            df_comp = pd.DataFrame(comparacao)
            st.dataframe(df_comp, use_container_width=True)
            
            st.markdown(f"""
            **Recomendações práticas:**
            - **{energia}:** {'Efeito fotoelétrico domina' if E < 100 else 'Compton domina' if E < 1000 else 'Produção de par domina'}
            - **{material}:** {'Excelente para baixas energias' if E < 200 and material == 'Chumbo (Pb)' else 'Bom custo-benefício' if material == 'Concreto' else 'Alta densidade'}
            - **Alternativas:** Considere blindagem em camadas para altas energias
            """)

# ============================================================
# MÓDULO 5: PERFIL E PROGRESSO
# ============================================================

def mostrar_perfil():
    """Exibe o perfil do jogador e progresso"""
    
    st.title("👤 SEU PERFIL DE FÍSICO MÉDICO")
    
    # Cabeçalho do perfil
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Avatar baseado no nível
        if st.session_state.nivel < 10:
            avatar = "👨‍🎓"
        elif st.session_state.nivel < 20:
            avatar = "👨‍⚕️"
        elif st.session_state.nivel < 30:
            avatar = "👨‍🔬"
        else:
            avatar = "👨‍🏫"
        
        st.markdown(f"# {avatar}")
        st.markdown(f"### Nível {st.session_state.nivel}")
        
        # Barra de XP
        xp_necessario = st.session_state.nivel * 100
        xp_atual = st.session_state.xp
        progresso = min(xp_atual / xp_necessario, 1.0)
        
        st.progress(progresso, text=f"XP: {xp_atual}/{xp_necessario}")
    
    with col2:
        st.subheader("📊 Estatísticas do Jogador")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("⭐ XP Total", st.session_state.xp_total)
            st.metric("💰 Dinheiro", f"R$ {st.session_state.dinheiro}")
        
        with col_b:
            st.metric("🎯 Missões", st.session_state.missoes_completas)
            st.metric("⚠️ Erros", st.session_state.erros_cometidos)
        
        with col_c:
            st.metric("🏥 Reputação", f"{st.session_state.reputacao}/100")
            st.metric("📈 Precisão", 
                     f"{(st.session_state.missoes_completas/(st.session_state.missoes_completas + st.session_state.erros_cometidos)*100):.1f}%" 
                     if st.session_state.missoes_completas + st.session_state.erros_cometidos > 0 else "0%")
    
    st.markdown("---")
    
    # Habilidades
    st.subheader("🎓 Suas Habilidades")
    
    for nome, dados in st.session_state.habilidades.items():
        col1, col2 = st.columns([1, 3])
        
        with col1:
            nivel = dados['nivel']
            # Ícone baseado no nível
            if nivel == 0:
                icone = "🔒"
                cor = "gray"
            elif nivel < 3:
                icone = "📖"
                cor = "blue"
            elif nivel < 5:
                icone = "📚"
                cor = "green"
            else:
                icone = "🏆"
                cor = "gold"
            
            st.markdown(f"### {icone} Nível {nivel}")
        
        with col2:
            # Barra de progresso da habilidade
            xp_hab = dados['xp']
            xp_necessario_hab = nivel * 50 + 50
            
            if nivel > 0:
                progresso_hab = min(xp_hab / xp_necessario_hab, 1.0)
                st.progress(progresso_hab, text=f"XP: {xp_hab}/{xp_necessario_hab}")
            
            # Fórmulas desbloqueadas
            if dados['formulas']:
                with st.expander(f"Fórmulas desbloqueadas ({len(dados['formulas'])})"):
                    for formula in dados['formulas']:
                        st.code(formula, language=None)
    
    st.markdown("---")
    
    # Inventário
    st.subheader("💼 Seu Inventário")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔬 Detectores")
        
        for nome, dados in st.session_state.inventario['detectores'].items():
            if dados['quantidade'] > 0:
                # Emojis para cada detector
                emojis = {
                    'geiger': '📡',
                    'camera_ionizacao': '⚡',
                    'nai': '💎'
                }
                
                st.markdown(f"{emojis.get(nome, '🔧')} **{nome.replace('_', ' ').title()}**")
                st.markdown(f"  Quantidade: {dados['quantidade']}")
                st.markdown(f"  Condição: {dados['condicao']}%")
    
    with col2:
        st.markdown("### 🧰 Ferramentas")
        
        for nome, disponivel in st.session_state.inventario['ferramentas'].items():
            if disponivel:
                emojis = {
                    'calculadora': '🧮',
                    'tabela_constantes': '📋',
                    'manual': '📖'
                }
                
                st.markdown(f"{emojis.get(nome, '🔧')} **{nome.replace('_', ' ').title()}**")
    
    st.markdown("---")
    
    # Conquistas
    st.subheader("🏅 Suas Conquistas")
    
    conquistas_info = {
        'primeiro_calculo': {
            'nome': 'Primeiro Cálculo',
            'descricao': 'Complete seu primeiro cálculo de dose',
            'icone': '🔢'
        },
        'detetive_perfeito': {
            'nome': 'Detetive Perfeito',
            'descricao': 'Encontre uma fonte perdida em menos de 5 tentativas',
            'icone': '🕵️'
        },
        'mestre_dosimetria': {
            'nome': 'Mestre da Dosimetria',
            'descricao': 'Calibre um acelerador com erro menor que 1%',
            'icone': '🎯'
        },
        'salvador_vidas': {
            'nome': 'Salvador de Vidas',
            'descricao': 'Complete 10 missões sem erros graves',
            'icone': '🦸'
        }
    }
    
    cols = st.columns(4)
    
    for idx, (chave, desbloqueada) in enumerate(st.session_state.conquistas.items()):
        info = conquistas_info[chave]
        
        with cols[idx % 4]:
            if desbloqueada:
                st.markdown(f"### {info['icone']}")
                st.markdown(f"**{info['nome']}**")
                st.markdown(f"*{info['descricao']}*")
                st.success("✅ Desbloqueada")
            else:
                st.markdown(f"### 🔒")
                st.markdown(f"**{info['nome']}**")
                st.markdown(f"*Conquista bloqueada*")
                st.info("Em progresso...")

# ============================================================
# MÓDULO 6: LOJA E RANKING
# ============================================================

def mostrar_loja():
    """Loja para compra de equipamentos e upgrades"""
    
    st.title("🛒 LOJA DE EQUIPAMENTOS")
    
    st.info(f"💰 **Seu saldo:** R$ {st.session_state.dinheiro}")
    
    # Itens disponíveis para compra
    itens = [
        {
            "nome": "Geiger-Müller Avançado",
            "descricao": "Compensação de energia, alarme sonoro",
            "preco": 800,
            "tipo": "detector",
            "chave": "geiger_avancado",
            "icone": "📡"
        },
        {
            "nome": "Câmara de Ionização Farmer",
            "descricao": "0,6 cm³, padrão ouro para dosimetria",
            "preco": 2500,
            "tipo": "detector",
            "chave": "camera_farmer",
            "icone": "⚡"
        },
        {
            "nome": "Detector NaI 2×2",
            "descricao": "Cristal 2×2 polegadas, para espectrometria",
            "preco": 6000,
            "tipo": "detector",
            "chave": "nai_2x2",
            "icone": "💎"
        },
        {
            "nome": "Manual Avançado",
            "descricao": "+10% XP em missões de cálculo",
            "preco": 1500,
            "tipo": "ferramenta",
            "chave": "manual_avancado",
            "icone": "📚"
        },
        {
            "nome": "Curso de Especialização",
            "descricao": "Aumenta todas as habilidades em 1 nível",
            "preco": 5000,
            "tipo": "upgrade",
            "chave": "curso_especializacao",
            "icone": "🎓"
        }
    ]
    
    # Exibir itens
    for i, item in enumerate(itens):
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            st.markdown(f"### {item['icone']}")
        
        with col2:
            st.markdown(f"**{item['nome']}**")
            st.markdown(f"*{item['descricao']}*")
        
        with col3:
            st.markdown(f"##### R$ {item['preco']}")
            
            # Verificar se já possui
            if item['tipo'] == 'detector':
                possui = st.session_state.inventario['detectores'].get(
                    item['chave'], {'quantidade': 0}
                )['quantidade'] > 0
            elif item['tipo'] == 'ferramenta':
                possui = st.session_state.inventario['ferramentas'].get(
                    item['chave'], False
                )
            else:
                possui = False
            
            if possui:
                st.success("✅ Adquirido")
            else:
                if st.button(f"Comprar", key=f"comprar_{i}"):
                    if st.session_state.dinheiro >= item['preco']:
                        st.session_state.dinheiro -= item['preco']
                        
                        # Adicionar ao inventário
                        if item['tipo'] == 'detector':
                            if item['chave'] not in st.session_state.inventario['detectores']:
                                st.session_state.inventario['detectores'][item['chave']] = {
                                    'quantidade': 0, 'condicao': 100
                                }
                            st.session_state.inventario['detectores'][item['chave']]['quantidade'] += 1
                        
                        elif item['tipo'] == 'ferramenta':
                            st.session_state.inventario['ferramentas'][item['chave']] = True
                        
                        elif item['tipo'] == 'upgrade':
                            # Aumentar todas as habilidades
                            for habilidade in st.session_state.habilidades.values():
                                if habilidade['nivel'] > 0:
                                    habilidade['nivel'] += 1
                        
                        st.success(f"✅ {item['nome']} adquirido com sucesso!")
                        st.rerun()
                    else:
                        st.error("💰 Saldo insuficiente!")

def mostrar_ranking():
    """Exibe ranking de jogadores (simulado)"""
    
    st.title("🏆 RANKING DOS FÍSICOS MÉDICOS")
    
    # Dados simulados do ranking
    ranking_data = [
        {"nome": "Dra. Carla Silva", "nivel": 42, "xp": 12500, "especialidade": "Medicina Nuclear"},
        {"nome": "Dr. Marcos Oliveira", "nivel": 38, "xp": 11000, "especialidade": "Radioterapia"},
        {"nome": "Dra. Ana Santos", "nivel": 35, "xp": 9800, "especialidade": "Radioproteção"},
        {"nome": "Você", "nivel": st.session_state.nivel, "xp": st.session_state.xp_total, 
         "especialidade": "Estagiário"},
        {"nome": "Dr. Roberto Lima", "nivel": 28, "xp": 7500, "especialidade": "Diagnóstico"},
        {"nome": "Dra. Fernanda Costa", "nivel": 25, "xp": 6200, "especialidade": "Medicina Nuclear"},
        {"nome": "Dr. Paulo Mendes", "nivel": 22, "xp": 5400, "especialidade": "Radioterapia"},
        {"nome": "Dra. Juliana Alves", "nivel": 19, "xp": 4300, "especialidade": "Radioproteção"},
        {"nome": "Dr. Ricardo Sousa", "nivel": 16, "xp": 3500, "especialidade": "Diagnóstico"},
        {"nome": "Dra. Beatriz Martins", "nivel": 12, "xp": 2800, "especialidade": "Medicina Nuclear"}
    ]
    
    # Ordenar por XP
    ranking_data.sort(key=lambda x: x["xp"], reverse=True)
    
    # Encontrar sua posição
    sua_posicao = next((i for i, jogador in enumerate(ranking_data) if jogador["nome"] == "Você"), -1)
    
    if sua_posicao >= 0:
        st.info(f"📊 **Sua posição no ranking:** #{sua_posicao + 1}")
    
    # Exibir top 10
    st.subheader("🥇 Top 10 Físicos Médicos")
    
    for i, jogador in enumerate(ranking_data[:10]):
        col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
        
        with col1:
            # Medalhas para os primeiros lugares
            if i == 0:
                st.markdown("🥇")
            elif i == 1:
                st.markdown("🥈")
            elif i == 2:
                st.markdown("🥉")
            else:
                st.markdown(f"**#{i+1}**")
        
        with col2:
            if jogador["nome"] == "Você":
                st.markdown(f"### 👤 **{jogador['nome']}**")
            else:
                st.markdown(f"**{jogador['nome']}**")
        
        with col3:
            st.markdown(f"**Nível {jogador['nivel']}**")
            st.markdown(f"⭐ {jogador['xp']:,} XP")
        
        with col4:
            # Emoji para especialidade
            emojis = {
                "Medicina Nuclear": "🔬",
                "Radioterapia": "🏥",
                "Radioproteção": "🛡️",
                "Diagnóstico": "📷",
                "Estagiário": "👨‍🎓"
            }
            st.markdown(f"{emojis.get(jogador['especialidade'], '👨‍⚕️')} {jogador['especialidade']}")
    
    # Estatísticas do ranking
    st.markdown("---")
    st.subheader("📈 Estatísticas do Ranking")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        media_nivel = np.mean([j["nivel"] for j in ranking_data])
        st.metric("Média de Nível", f"{media_nivel:.1f}")
    
    with col2:
        media_xp = np.mean([j["xp"] for j in ranking_data])
        st.metric("Média de XP", f"{media_xp:,.0f}")
    
    with col3:
        especialidades = [j["especialidade"] for j in ranking_data]
        mais_comum = max(set(especialidades), key=especialidades.count)
        st.metric("Especialidade mais comum", mais_comum)
    
    # Progresso em relação ao topo
    if sua_posicao >= 0:
        st.markdown("---")
        
        xp_top = ranking_data[0]["xp"]
        seu_xp = st.session_state.xp_total
        
        if seu_xp < xp_top:
            percentual = (seu_xp / xp_top) * 100
            st.progress(percentual/100, text=f"Progresso em relação ao 1º lugar: {percentual:.1f}%")
            
            xp_necessario = xp_top - seu_xp
            st.info(f"⭐ Você precisa de mais **{xp_necessario:,.0f} XP** para alcançar o 1º lugar!")

# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def main():
    """Função principal do jogo"""
    
    # Configuração da página
    st.set_page_config(
        page_title="Físico Médico: A Missão",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inicializar sessão
    inicializar_sessao()
    
    # Barra lateral - Navegação
    with st.sidebar:
        st.title("🏥 Físico Médico: A Missão")
        st.markdown("---")
        
        # Menu principal
        menu = st.radio(
            "🎮 **MENU PRINCIPAL**",
            ["📋 Painel Principal", "🎯 Missões", "🧮 Calculadoras", 
             "🔬 Simuladores", "👤 Meu Perfil", "🛒 Loja", "🏆 Ranking"]
        )
        
        st.markdown("---")
        
        # Status rápido
        st.markdown("### 📊 Status Rápido")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Nível", st.session_state.nivel)
        with col2:
            st.metric("XP", st.session_state.xp_total)
        
        st.markdown(f"💰 **Saldo:** R$ {st.session_state.dinheiro}")
        st.markdown(f"🏥 **Reputação:** {st.session_state.reputacao}/100")
        
        st.markdown("---")
        
        # Botão de ajuda
        if st.button("🆘 Tutorial Rápido"):
            st.info("""
            **Como jogar:**
            1. Complete missões para ganhar XP e dinheiro
            2. Use as calculadoras para aprender os conceitos
            3. Compre equipamentos na loja
            4. Suba de nível e desbloqueie novas missões
            
            **Dica:** Sempre verifique suas unidades nos cálculos!
            """)
        
        # Botão de reset (apenas para desenvolvimento)
        if st.button("🔄 Resetar Jogo (DEV)"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Navegação para páginas
    if menu == "📋 Painel Principal":
        mostrar_painel_principal()
    
    elif menu == "🎯 Missões":
        st.title("🎯 MISSÕES DISPONÍVEIS")
        
        # Seleção de missão
        missao_selecionada = st.selectbox(
            "Escolha uma missão para iniciar:",
            ["🔬 Emergência na Farmácia Radioativa (Nível 1)",
             "🏥 Calibração de Acelerador Linear (Nível 2)",
             "🕵️ Detetive Radioativo: Fonte Perdida (Nível 1)"]
        )
        
        if missao_selecionada == "🔬 Emergência na Farmácia Radioativa (Nível 1)":
            st.session_state.missao_atual = "farmacia_radioativa"
        elif missao_selecionada == "🏥 Calibração de Acelerador Linear (Nível 2)":
            st.session_state.missao_atual = "calibracao_acelerador"
        elif missao_selecionada == "🕵️ Detetive Radioativo: Fonte Perdida (Nível 1)":
            st.session_state.missao_atual = "fonte_perdida"
        
        # Executar missão se selecionada
        if 'missao_atual' in st.session_state:
            if st.session_state.missao_atual == "farmacia_radioativa":
                missao_farmacia_radioativa()
            elif st.session_state.missao_atual == "calibracao_acelerador":
                missao_calibracao_acelerador()
            elif st.session_state.missao_atual == "fonte_perdida":
                missao_fonte_perdida()
            
            # Botão para voltar
            if st.button("🏠 Voltar ao Menu"):
                st.session_state.missao_atual = None
                st.rerun()
    
    elif menu == "🧮 Calculadoras":
        mostrar_calculadoras()
    
    elif menu == "🔬 Simuladores":
        mostrar_simuladores()
    
    elif menu == "👤 Meu Perfil":
        mostrar_perfil()
    
    elif menu == "🛒 Loja":
        mostrar_loja()
    
    elif menu == "🏆 Ranking":
        mostrar_ranking()
    
    # Rodapé
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
        🏥 <b>Físico Médico: A Missão</b> - Jogo Educativo de Física Radiológica<br>
        Desenvolvido para aprendizado prático | Versão 1.0.0
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# EXECUÇÃO DO JOGO
# ============================================================

if __name__ == "__main__":
    main()