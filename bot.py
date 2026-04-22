import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import asyncio

# --- SERVIDOR WEB ---
app = Flask(__name__)

# COLA AQUI O TEU TOKEN DO BOTFATHER
TOKEN = os.environ['TOKEN']
URL = "https://bot-estetica.onrender.com"
bot_app = Application.builder().token(TOKEN).build()

# ========== WEBHOOK ROUTE ==========
@app.route(f'/{TOKEN}', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    await bot_app.process_update(update)
    return 'ok', 200
    
# DADOS MOCKADOS - o PAIS_ATUAL vai mudar quando clica
PAIS_ATUAL = "Afeganistão 🇦🇫"
SALDO = "0 USD"

# ========== PARTE DOS SERVIÇOS - NÃO MEXER MAIS ==========
SERVICOS_VALIDOS = [
    "whatsapp", "facebook", "google", "youtube", "telegram", "airbnb", "amazon",
    "instagram", "threads", "microsoft", "tinder", "tiktok", "douyin", "netflix", 
    "discord", "linkedin", "twitter", "olx", "uber", "shopee", "paypal", "alipay", 
    "alibaba", "blizzard", "bigo", "bigolive", "grindr", "coinbase", "deliveroo",
    "aol", "baidu", "bolt", "careem", "craigslist", "ebay", "foodpanda", "grab", 
    "hily", "imo", "jdcom", "kakaotalk", "line", "mailru", "naver", "nike", 
    "nttgame", "offgamers", "openai", "papara", "paycell", "paytm", "pof", "skout",
    "snapchat", "steam", "tencent", "qq", "viber", "vk", "wechat", "weibo", 
    "wolt", "yahoo", "yalla", "yandex", "zoho"
]

SERVICOS_PAGINA_1 = [
    [("🟢 Whatsapp", "srv_whatsapp"), ("📘 Facebook", "srv_facebook"), ("🔍 Google,youtub...", "srv_google")],
    [("✈️ Telegram", "srv_telegram"), ("🏠 Airbnb", "srv_airbnb"), ("📦 Amazon", "srv_amazon")],
    [("📷 Instagram+Th...", "srv_instagram"), ("🪟 Microsoft", "srv_microsoft"), ("🔥 Tinder", "srv_tinder")],
    [("🎵 TikTok/Douyin", "srv_tiktok"), ("🎬 Netflix", "srv_netflix"), ("🎮 Discord", "srv_discord")],
    [("💼 LinkedIN", "srv_linkedin"), ("𝕏 Twitter", "srv_twitter"), ("🛒 OLX", "srv_olx")],
    [("🚗 Uber", "srv_uber"), ("🛍️ Shopee", "srv_shopee"), ("💳 PayPal", "srv_paypal")],
    [("💰 Alipay/Alibaba/1688", "srv_alipay"), ("❄️ Blizzard", "srv_blizzard"), ("📹 BIGO LIVE", "srv_bigo")],
    [("🏳️‍🌈 Grindr", "srv_grindr"), ("🪙 Coinbase", "srv_coinbase"), ("🛵 Deliveroo", "srv_deliveroo")],
    [("Próxima Página ➡️", "page_2")]
]

SERVICOS_PAGINA_2 = [
    [("📧 AOL", "srv_aol"), ("🐻 Baidu", "srv_baidu"), ("⚡ Bolt", "srv_bolt")],
    [("🚕 Careem", "srv_careem"), ("📋 Craigslist", "srv_craigslist"), ("🏷️ EBay", "srv_ebay")],
    [("🐼 Foodpanda", "srv_foodpanda"), ("🚗 Grab", "srv_grab"), ("💜 Hily", "srv_hily")],
    [("💬 Imo", "srv_imo"), ("📦 JDcom", "srv_jdcom"), ("💛 KakaoTalk", "srv_kakaotalk")],
    [("💚 Line messenger", "srv_line"), ("📧 Mail.ru", "srv_mailru"), ("🟢 Naver", "srv_naver")],
    [("✔️ Nike", "srv_nike"), ("⚔️ Nttgame", "srv_nttgame"), ("🎮 OffGamers", "srv_offgamers")],
    [("🌀 OpenAI", "srv_openai"), ("💳 Papara", "srv_papara"), ("📱 Paycell", "srv_paycell")],
    [("💰 Paytm", "srv_paytm"), ("🐟 Pof.com", "srv_pof"), ("👥 Skout", "srv_skout")],
    [("⬅️ Página Anterior", "page_1"), ("Próxima Página ➡️", "page_3")]
]

SERVICOS_PAGINA_3 = [
    [("👻 Snapchat", "srv_snapchat"), ("🎮 Steam", "srv_steam"), ("🐧 Tencent QQ", "srv_tencent")],
    [("📞 Viber", "srv_viber"), ("🔵 Vk.com", "srv_vk"), ("💚 WeChat", "srv_wechat")],
    [("👁️ Weibo", "srv_weibo"), ("🛵 Wolt", "srv_wolt"), ("📧 Yahoo", "srv_yahoo")],
    [("🎤 Yalla", "srv_yalla"), ("🚕 Yandex/Uber", "srv_yandex"), ("📊 Zoho", "srv_zoho")],
    [("⬅️ Página Anterior", "page_2")]
]

def criar_teclado_servicos(pagina):
    paginas = {1: SERVICOS_PAGINA_1, 2: SERVICOS_PAGINA_2, 3: SERVICOS_PAGINA_3}
    botoes = paginas.get(pagina, SERVICOS_PAGINA_1)
    
    keyboard = []
    for linha in botoes:
        linha_botoes = [InlineKeyboardButton(texto, callback_data=callback) for texto, callback in linha]
        keyboard.append(linha_botoes)
    return InlineKeyboardMarkup(keyboard)

def texto_servicos():
    global PAIS_ATUAL, SALDO
    return f"""PAÍS ATUAL {PAIS_ATUAL} /paises
SALDO {SALDO} 💰 /recarregar
ESCOLHA O SERVIÇO PARA RECEBER SMS
💡 Você também pode digitar o nome do serviço diretamente! Ex: WhatsApp"""

# ========== PARTE DOS PAÍSES - NOVA ==========
PAISES_PAGINA_1 = [
    [("AFEGANISTÃO 🇦🇫", "pais_Afeganistão 🇦🇫"), ("ALBÂNIA 🇦🇱", "pais_Albânia 🇦🇱")],
    [("ALEMANHA 🇩🇪", "pais_Alemanha 🇩🇪"), ("ANGOLA 🇦🇴", "pais_Angola 🇦🇴")],
    [("ANGUILLA 🇦🇮", "pais_Anguilla 🇦🇮"), ("ANTÍGUA E BARBUDA 🇦🇬", "pais_Antígua e Barbuda 🇦🇬")],
    [("ARGENTINA 🇦🇷", "pais_Argentina 🇦🇷"), ("ARGÉLIA 🇩🇿", "pais_Argélia 🇩🇿")],
    [("ARMÊNIA 🇦🇲", "pais_Armênia 🇦🇲"), ("ARUBA 🇦🇼", "pais_Aruba 🇦🇼")],
    [("AUSTRÁLIA 🇦🇺", "pais_Austrália 🇦🇺"), ("AZERBAIJÃO 🇦🇿", "pais_Azerbaijão 🇦🇿")],
    [("BAHAMAS 🇧🇸", "pais_Bahamas 🇧🇸"), ("BAHREIN 🇧🇭", "pais_Bahrein 🇧🇭")],
    [("BANGLADESH 🇧🇩", "pais_Bangladesh 🇧🇩"), ("BARBADOS 🇧🇧", "pais_Barbados 🇧🇧")],
    [("BELARUS 🇧🇾", "pais_Belarus 🇧🇾"), ("BELIZE 🇧🇿", "pais_Belize 🇧🇿")],
    [("BENIM 🇧🇯", "pais_Benim 🇧🇯"), ("BOLÍVIA 🇧🇴", "pais_Bolívia 🇧🇴")],
    [("Próxima Página ➡️", "pais_page_2")]
]

PAISES_PAGINA_2 = [
    [("BOTSUANA 🇧🇼", "pais_Botsuana 🇧🇼"), ("BRASIL 🇧🇷", "pais_Brasil 🇧🇷")],
    [("BRUNEI 🇧🇳", "pais_Brunei 🇧🇳"), ("BULGÁRIA 🇧🇬", "pais_Bulgária 🇧🇬")],
    [("BURQUINA FASO 🇧🇫", "pais_Burquina Faso 🇧🇫"), ("BURUNDI 🇧🇮", "pais_Burundi 🇧🇮")],
    [("BUTÃO 🇧🇹", "pais_Butão 🇧🇹"), ("BÉLGICA 🇧🇪", "pais_Bélgica 🇧🇪")],
    [("BÓSNIA E HERZEGOVINA 🇧🇦", "pais_Bósnia e Herzegovina 🇧🇦"), ("CABO VERDE 🇨🇻", "pais_Cabo Verde 🇨🇻")],
    [("CAMARÕES 🇨🇲", "pais_Camarões 🇨🇲"), ("CAMBOJA 🇰🇭", "pais_Camboja 🇰🇭")],
    [("CANADÁ 🇨🇦", "pais_Canadá 🇨🇦"), ("CAZAQUISTÃO 🇰🇿", "pais_Cazaquistão 🇰🇿")],
    [("CHADE 🇹🇩", "pais_Chade 🇹🇩"), ("CHILE 🇨🇱", "pais_Chile 🇨🇱")],
    [("CHINA 🇨🇳", "pais_China 🇨🇳"), ("CHIPRE 🇨🇾", "pais_Chipre 🇨🇾")],
    [("COLÔMBIA 🇨🇴", "pais_Colômbia 🇨🇴"), ("COMORES 🇰🇲", "pais_Comores 🇰🇲")],
    [("⬅️ Página Anterior", "pais_page_1"), ("Próxima Página ➡️", "pais_page_3")]
]

PAISES_PAGINA_3 = [
    [("COSTA DO MARFIM 🇨🇮", "pais_Costa do Marfim 🇨🇮"), ("COSTA RICA 🇨🇷", "pais_Costa Rica 🇨🇷")],
    [("CROÁCIA 🇭🇷", "pais_Croácia 🇭🇷"), ("DINAMARCA 🇩🇰", "pais_Dinamarca 🇩🇰")],
    [("DJIBOUTI 🇩🇯", "pais_Djibouti 🇩🇯"), ("DOMINICA 🇩🇲", "pais_Dominica 🇩🇲")],
    [("EGITO 🇪🇬", "pais_Egito 🇪🇬"), ("EL SALVADOR 🇸🇻", "pais_El Salvador 🇸🇻")],
    [("EMIRADOS ÁRABES UNIDOS 🇦🇪", "pais_Emirados Árabes Unidos 🇦🇪"), ("EQUADOR 🇪🇨", "pais_Equador 🇪🇨")],
    [("ERITREIA 🇪🇷", "pais_Eritreia 🇪🇷"), ("ESLOVÁQUIA 🇸🇰", "pais_Eslováquia 🇸🇰")],
    [("ESLOVÊNIA 🇸🇮", "pais_Eslovênia 🇸🇮"), ("ESPANHA 🇪🇸", "pais_Espanha 🇪🇸")],
    [("ESTÔNIA 🇪🇪", "pais_Estônia 🇪🇪"), ("ESWATINI 🇸🇿", "pais_Eswatini 🇸🇿")],
    [("ETIÓPIA 🇪🇹", "pais_Etiópia 🇪🇹"), ("EUA 🇺🇸", "pais_EUA 🇺🇸")],
    [("FIJI 🇫🇯", "pais_Fiji 🇫🇯"), ("FILIPINAS 🇵🇭", "pais_Filipinas 🇵🇭")],
    [("⬅️ Página Anterior", "pais_page_2"), ("Próxima Página ➡️", "pais_page_4")]
]

PAISES_PAGINA_4 = [
    [("FINLÂNDIA 🇫🇮", "pais_Finlândia 🇫🇮"), ("FRANÇA 🇫🇷", "pais_França 🇫🇷")],
    [("GABÃO 🇬🇦", "pais_Gabão 🇬🇦"), ("GANA 🇬🇭", "pais_Gana 🇬🇭")],
    [("GEÓRGIA 🇬🇪", "pais_Geórgia 🇬🇪"), ("GIBRALTAR 🇬🇮", "pais_Gibraltar 🇬🇮")],
    [("GRANADA 🇬🇩", "pais_Granada 🇬🇩"), ("GRÉCIA 🇬🇷", "pais_Grécia 🇬🇷")],
    [("GUADALUPE 🇬🇵", "pais_Guadalupe 🇬🇵"), ("GUATEMALA 🇬🇹", "pais_Guatemala 🇬🇹")],
    [("GUIANA FRANCESA 🇬🇫", "pais_Guiana Francesa 🇬🇫"), ("GUIANA 🇬🇾", "pais_Guiana 🇬🇾")],
    [("GUINÉ-BISSAU 🇬🇼", "pais_Guiné-Bissau 🇬🇼"), ("GUINÉ EQUATORIAL 🇬🇶", "pais_Guiné Equatorial 🇬🇶")],
    [("GUINÉ 🇬🇳", "pais_Guiné 🇬🇳"), ("GÂMBIA 🇬🇲", "pais_Gâmbia 🇬🇲")],
    [("HAITI 🇭🇹", "pais_Haiti 🇭🇹"), ("HOLANDA 🇳🇱", "pais_Holanda 🇳🇱")],
    [("HONDURAS 🇭🇳", "pais_Honduras 🇭🇳"), ("HONG KONG 🇭🇰", "pais_Hong Kong 🇭🇰")],
    [("⬅️ Página Anterior", "pais_page_3"), ("Próxima Página ➡️", "pais_page_5")]
]

PAISES_PAGINA_5 = [
    [("HUNGRIA 🇭🇺", "pais_Hungria 🇭🇺"), ("INDONÉSIA 🇮🇩", "pais_Indonésia 🇮🇩")],
    [("IRAQUE 🇮🇶", "pais_Iraque 🇮🇶"), ("IRLANDA 🇮🇪", "pais_Irlanda 🇮🇪")],
    [("IRÃ 🇮🇷", "pais_Irã 🇮🇷"), ("ISRAEL 🇮🇱", "pais_Israel 🇮🇱")],
    [("ITÁLIA 🇮🇹", "pais_Itália 🇮🇹"), ("IÊMEN 🇾🇪", "pais_Iêmen 🇾🇪")],
    [("JAMAICA 🇯🇲", "pais_Jamaica 🇯🇲"), ("JAPÃO 🇯🇵", "pais_Japão 🇯🇵")],
    [("JORDÂNIA 🇯🇴", "pais_Jordânia 🇯🇴"), ("KUWAIT 🇰🇼", "pais_Kuwait 🇰🇼")],
    [("LAOS 🇱🇦", "pais_Laos 🇱🇦"), ("LESOTO 🇱🇸", "pais_Lesoto 🇱🇸")],
    [("LETÔNIA 🇱🇻", "pais_Letônia 🇱🇻"), ("LIBÉRIA 🇱🇷", "pais_Libéria 🇱🇷")],
    [("LITUÂNIA 🇱🇹", "pais_Lituânia 🇱🇹"), ("LUXEMBURGO 🇱🇺", "pais_Luxemburgo 🇱🇺")],
    [("LÍBANO 🇱🇧", "pais_Líbano 🇱🇧"), ("LÍBIA 🇱🇾", "pais_Líbia 🇱🇾")],
    [("⬅️ Página Anterior", "pais_page_4"), ("Próxima Página ➡️", "pais_page_6")]
]

PAISES_PAGINA_6 = [
    [("MACAU 🇲🇴", "pais_Macau 🇲🇴"), ("MACEDÔNIA DO NORTE 🇲🇰", "pais_Macedônia do Norte 🇲🇰")],
    [("MADAGASCAR 🇲🇬", "pais_Madagascar 🇲🇬"), ("MALAWI 🇲🇼", "pais_Malawi 🇲🇼")],
    [("MALDIVAS 🇲🇻", "pais_Maldivas 🇲🇻"), ("MALI 🇲🇱", "pais_Mali 🇲🇱")],
    [("MALTA 🇲🇹", "pais_Malta 🇲🇹"), ("MALÁSIA 🇲🇾", "pais_Malásia 🇲🇾")],
    [("MARROCOS 🇲🇦", "pais_Marrocos 🇲🇦"), ("MAURITÂNIA 🇲🇷", "pais_Mauritânia 🇲🇷")],
    [("MAURÍCIO 🇲🇺", "pais_Maurício 🇲🇺"), ("MIANMAR 🇲🇲", "pais_Mianmar 🇲🇲")],
    [("MOLDÁVIA 🇲🇩", "pais_Moldávia 🇲🇩"), ("MONGÓLIA 🇲🇳", "pais_Mongólia 🇲🇳")],
    [("MONTENEGRO 🇲🇪", "pais_Montenegro 🇲🇪"), ("MONTSERRAT 🇲🇸", "pais_Montserrat 🇲🇸")],
    [("MOÇAMBIQUE 🇲🇿", "pais_Moçambique 🇲🇿"), ("MÉXICO 🇲🇽", "pais_México 🇲🇽")],
    [("MÔNACO 🇲🇨", "pais_Mônaco 🇲🇨"), ("NAMÍBIA 🇳🇦", "pais_Namíbia 🇳🇦")],
    [("⬅️ Página Anterior", "pais_page_5"), ("Próxima Página ➡️", "pais_page_7")]
]

PAISES_PAGINA_7 = [
    [("NEPAL 🇳🇵", "pais_Nepal 🇳🇵"), ("NICARÁGUA 🇳🇮", "pais_Nicarágua 🇳🇮")],
    [("NIGÉRIA 🇳🇬", "pais_Nigéria 🇳🇬"), ("NIUE 🇳🇺", "pais_Niue 🇳🇺")],
    [("NORUEGA 🇳🇴", "pais_Noruega 🇳🇴"), ("NOVA ZELÂNDIA 🇳🇿", "pais_Nova Zelândia 🇳🇿")],
    [("NÍGER 🇳🇪", "pais_Níger 🇳🇪"), ("OMÃ 🇴🇲", "pais_Omã 🇴🇲")],
    [("PALESTINA 🇵🇸", "pais_Palestina 🇵🇸"), ("PANAMÁ 🇵🇦", "pais_Panamá 🇵🇦")],
    [("PAPUA NOVA GUINÉ 🇵🇬", "pais_Papua Nova Guiné 🇵🇬"), ("PAQUISTÃO 🇵🇰", "pais_Paquistão 🇵🇰")],
    [("PARAGUAI 🇵🇾", "pais_Paraguai 🇵🇾"), ("PERU 🇵🇪", "pais_Peru 🇵🇪")],
    [("POLÔNIA 🇵🇱", "pais_Polônia 🇵🇱"), ("PORTO RICO 🇵🇷", "pais_Porto Rico 🇵🇷")],
    [("PORTUGAL 🇵🇹", "pais_Portugal 🇵🇹"), ("QUIRGUISTÃO 🇰🇬", "pais_Quirguistão 🇰🇬")],
    [("QUÊNIA 🇰🇪", "pais_Quênia 🇰🇪"), ("REINO UNIDO 🇬🇧", "pais_Reino Unido 🇬🇧")],
    [("⬅️ Página Anterior", "pais_page_6"), ("Próxima Página ➡️", "pais_page_8")]
]

PAISES_PAGINA_8 = [
    [("REPÚBLICA CENTRO-AFRICANA 🇨🇫", "pais_República Centro-Africana 🇨🇫"), ("REPÚBLICA DEMOCRÁTICA DO CONGO 🇨🇩", "pais_República Democrática do Congo 🇨🇩")],
    [("REPÚBLICA DO CONGO 🇨🇬", "pais_República do Congo 🇨🇬"), ("REPÚBLICA DOMINICANA 🇩🇴", "pais_República Dominicana 🇩🇴")],
    [("REPÚBLICA TCHECA 🇨🇿", "pais_República Tcheca 🇨🇿"), ("REUNIÃO 🇷🇪", "pais_Reunião 🇷🇪")],
    [("ROMÊNIA 🇷🇴", "pais_Romênia 🇷🇴"), ("RUANDA 🇷🇼", "pais_Ruanda 🇷🇼")],
    [("SAMOA 🇼🇸", "pais_Samoa 🇼🇸"), ("SANTA LÚCIA 🇱🇨", "pais_Santa Lúcia 🇱🇨")],
    [("SENEGAL 🇸🇳", "pais_Senegal 🇸🇳"), ("SERRA LEOA 🇸🇱", "pais_Serra Leoa 🇸🇱")],
    [("SEYCHELLES 🇸🇨", "pais_Seychelles 🇸🇨"), ("SINGAPURA 🇸🇬", "pais_Singapura 🇸🇬")],
    [("SOMÁLIA 🇸🇴", "pais_Somália 🇸🇴"), ("SRI LANKA 🇱🇰", "pais_Sri Lanka 🇱🇰")],
    [("SUDÃO DO SUL 🇸🇸", "pais_Sudão do Sul 🇸🇸"), ("SUDÃO 🇸🇩", "pais_Sudão 🇸🇩")],
    [("SURINAME 🇸🇷", "pais_Suriname 🇸🇷"), ("SUÉCIA 🇸🇪", "pais_Suécia 🇸🇪")],
    [("⬅️ Página Anterior", "pais_page_7"), ("Próxima Página ➡️", "pais_page_9")]
]

PAISES_PAGINA_9 = [
    [("SUÍÇA 🇨🇭", "pais_Suíça 🇨🇭"), ("SÃO CRISTÓVÃO E NÉVIS 🇰🇳", "pais_São Cristóvão e Névis 🇰🇳")],
    [("SÃO TOMÉ E PRÍNCIPE 🇸🇹", "pais_São Tomé e Príncipe 🇸🇹"), ("SÃO VICENTE E GRANADINAS 🇻🇨", "pais_São Vicente e Granadinas 🇻🇨")],
    [("SÉRVIA 🇷🇸", "pais_Sérvia 🇷🇸"), ("SÍRIA 🇸🇾", "pais_Síria 🇸🇾")],
    [("TAILÂNDIA 🇹🇭", "pais_Tailândia 🇹🇭"), ("TAJIQUISTÃO 🇹🇯", "pais_Tajiquistão 🇹🇯")],
    [("TANZÂNIA 🇹🇿", "pais_Tanzânia 🇹🇿"), ("TIMOR-LESTE 🇹🇱", "pais_Timor-Leste 🇹🇱")],
    [("TOGO 🇹🇬", "pais_Togo 🇹🇬"), ("TRINIDAD E TOBAGO 🇹🇹", "pais_Trinidad e Tobago 🇹🇹")],
    [("TUNÍSIA 🇹🇳", "pais_Tunísia 🇹🇳"), ("TURQUEMENISTÃO 🇹🇲", "pais_Turquemenistão 🇹🇲")],
    [("TURQUIA 🇹🇷", "pais_Turquia 🇹🇷"), ("UCRÂNIA 🇺🇦", "pais_Ucrânia 🇺🇦")],
    [("UGANDA 🇺🇬", "pais_Uganda 🇺🇬"), ("URUGUAI 🇺🇾", "pais_Uruguai 🇺🇾")],
    [("UZBEQUISTÃO 🇺🇿", "pais_Uzbequistão 🇺🇿"), ("VENEZUELA 🇻🇪", "pais_Venezuela 🇻🇪")],
    [("⬅️ Página Anterior", "pais_page_8")]
]

def criar_teclado_paises(pagina):
    paginas = {
        1: PAISES_PAGINA_1, 2: PAISES_PAGINA_2, 3: PAISES_PAGINA_3,
        4: PAISES_PAGINA_4, 5: PAISES_PAGINA_5, 6: PAISES_PAGINA_6,
        7: PAISES_PAGINA_7, 8: PAISES_PAGINA_8, 9: PAISES_PAGINA_9
    }
    botoes = paginas.get(pagina, PAISES_PAGINA_1)
    
    keyboard = []
    for linha in botoes:
        linha_botoes = [InlineKeyboardButton(texto, callback_data=callback) for texto, callback in linha]
        keyboard.append(linha_botoes)
    return InlineKeyboardMarkup(keyboard)

def texto_paises():
    global PAIS_ATUAL
    return f"""PAÍS ATUAL {PAIS_ATUAL}
📊 185 países com números disponíveis, mude para:"""

# ========== COMANDOS ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bem-vindo! 👋\n\nUsa o menu azul pra navegar:\n/services - Receber Sms 💬\n/paises - Países Disponíveis 🇧🇷\n/recarregar - Recarregar Saldo 💰"
    )

async def recarregar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        f"Agradecemos o vosso interesse!!!!!\n"
        f"Informamos que o carregamento minimo sao de 10 USD."
    )

    keyboard = [
        [InlineKeyboardButton("💰 Recarregar com Crypto", callback_data="recarregar_crypto")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(texto, reply_markup=reply_markup)

async def paises(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        texto_paises(),
        reply_markup=criar_teclado_paises(1)
    )

async def services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        texto_servicos(),
        reply_markup=criar_teclado_servicos(1)
    )

async def suport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("💬 Falar com Atendimento", url="https://t.me/cigano1970")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Atendimento:",
        reply_markup=reply_markup
    )

# ========== BOTÕES CLICÁVEIS ==========
async def botoes_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global PAIS_ATUAL
    query = update.callback_query
    data = query.data
    
    # Paginação SERVIÇOS - NÃO MEXER
    if data == "page_1":
        await query.answer()
        await query.edit_message_text(texto_servicos(), reply_markup=criar_teclado_servicos(1))
    elif data == "page_2":
        await query.answer()
        await query.edit_message_text(texto_servicos(), reply_markup=criar_teclado_servicos(2))
    elif data == "page_3":
        await query.answer()
        await query.edit_message_text(texto_servicos(), reply_markup=criar_teclado_servicos(3))
    # Clique num serviço - NÃO MEXER
    elif data.startswith("srv_"):
        await query.answer(text="modo estudo", show_alert=False)
    
    # Paginação PAÍSES - NOVA
    elif data == "pais_page_1":
        await query.answer()
        await query.edit_message_text(texto_paises(), reply_markup=criar_teclado_paises(1))
    elif data == "pais_page_2":
        await query.answer()
        await query.edit_message_text(texto_paises(), reply_markup=criar_teclado_paises(2))
    elif data == "pais_page_3":
        await query.answer()
        await query.edit_message_text(texto_paises(), reply_markup=criar_teclado_paises(3))
    elif data == "pais_page_4":
        await query.answer()
        await query.edit_message_text(texto_paises(), reply_markup=criar_teclado_paises(4))
    elif data == "pais_page_5":
        await query.answer()
        await query.edit_message_text(texto_paises(), reply_markup=criar_teclado_paises(5))
    elif data == "pais_page_6":
        await query.answer()
        await query.edit_message_text(texto_paises(), reply_markup=criar_teclado_paises(6))
    elif data == "pais_page_7":
        await query.answer()
        await query.edit_message_text(texto_paises(), reply_markup=criar_teclado_paises(7))
    elif data == "pais_page_8":
        await query.answer()
        await query.edit_message_text(texto_paises(), reply_markup=criar_teclado_paises(8))
    elif data == "pais_page_9":
        await query.answer()
        await query.edit_message_text(texto_paises(), reply_markup=criar_teclado_paises(9))
    # Clicou num país - MUDA O PAÍS E ABRE O MENU DE SMS
    elif data.startswith("pais_"):
        PAIS_ATUAL = data.replace("pais_", "")
        await query.answer()
        await query.edit_message_text(
            texto_servicos(),
            reply_markup=criar_teclado_servicos(1)
        )
    
    # RECARREGAR CRYPTO - CORRIGIDO
    elif data == "recarregar_crypto":
        texto_crypto = (
            f"Obrigado por recarregar!\n\n"
            f"💰 Moeda: Token\n"
            f"📬 Endereço: 666666666666666666666\n\n"
            f"Envie o valor exato para o endereço acima.\n"
            f"Após 1 confirmação o saldo será creditado."
        )
        
        keyboard = [[InlineKeyboardButton("🔙 Voltar", callback_data="voltar_recarregar")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.answer()
        await query.edit_message_text(texto_crypto, reply_markup=reply_markup)
    
    # VOLTAR PRO MENU RECARREGAR
    elif data == "voltar_recarregar":
        texto = (
            f"Agradecemos o vosso interesse!!!!!\n"
            f"Informamos que o carregamento minimo sao de 10 USD."
        )
        keyboard = [[InlineKeyboardButton("💰 Recarregar com Crypto", callback_data="recarregar_crypto")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.answer()
        await query.edit_message_text(texto, reply_markup=reply_markup)
    
    # VER SALDO
    elif data == "ver_saldo":
        global SALDO
        await query.answer()
        await query.edit_message_text(
            f"💳 Saldo atual: {SALDO}\n\nUse /recarregar para adicionar saldo.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💰 Recarregar com Crypto", callback_data="recarregar_crypto")]
            ])
        )

# ========== TEXTO DIGITADO - SÓ PRA SERVIÇOS ==========
async def texto_digitado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower().strip()
    texto_limpo = ''.join(e for e in texto if e.isalnum())
    
    for servico in SERVICOS_VALIDOS:
        if servico in texto_limpo:
            await update.message.reply_text(f"✅ Serviço selecionado: {servico.title()}\n\nmodo estudo")
            return
    
    await update.message.reply_text("Serviço não encontrado. Usa /services pra ver a lista completa.")

        
       # ========== REGISTRA HANDLERS ==========
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("recarregar", recarregar))
bot_app.add_handler(CommandHandler("paises", paises))
bot_app.add_handler(CommandHandler("services", services))
bot_app.add_handler(CommandHandler("suport", suport))
bot_app.add_handler(CallbackQueryHandler(botoes_callback))
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, texto_digitado))

@app.route('/')
def home():
    return "Bot Estetica Online", 200

# ========== MAIN ==========
# ========== MAIN ==========
def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host="0.0.0.0", port=port)

async def setup():
    await bot_app.bot.delete_webhook(drop_pending_updates=True)
    await asyncio.sleep(1)
    await bot_app.bot.set_webhook(url=f"{URL}/{TOKEN}")
    await bot_app.initialize()
    await bot_app.start()
    print("Webhook setado. Bot vivo 24h.", flush=True)

if __name__ == "__main__":
    import threading
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    asyncio.run(setup())
    
    flask_thread.join()
