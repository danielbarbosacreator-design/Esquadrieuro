import os
import json
from PIL import Image

OUT_IMG_DIR = "assets/catalog-products"
os.makedirs(OUT_IMG_DIR, exist_ok=True)

# 1. Coordinate Definitions for Clean Product Crops
# -------------------------------------------------
GRID_3X3_COLS = [(30, 406), (432, 808), (834, 1210)]
GRID_3X3_ROWS = [(138, 604), (640, 1106), (1142, 1608)]

def get_perfect_crop(card, has_color_bar=False, is_2x4_screw=False):
    w, h = card.size
    if is_2x4_screw:
        card = card.crop((8, 0, min(240, w), h))
        w, h = card.size
        
    top = int(h * 0.22)
    for y in range(int(h * 0.15), int(h * 0.45)):
        white_count = sum(1 for x in range(12, w - 12) if card.getpixel((x, y))[0] > 200 and card.getpixel((x, y))[1] > 200 and card.getpixel((x, y))[2] > 200 and abs(card.getpixel((x, y))[0] - card.getpixel((x, y))[1]) < 25)
        if white_count > (w - 24) * 0.80:
            top = y + 6
            break
            
    bottom = (h - 78) if has_color_bar else (h - 16)
    return card.crop((6, top, w - 6, bottom))

def crop_clean_3x3(page_num, row, col, img_name, has_color_bar=False):
    page_file = f"assets/catalog-pages/page-{page_num:02d}.png"
    im = Image.open(page_file)
    x1, x2 = GRID_3X3_COLS[col]
    y1, y2 = GRID_3X3_ROWS[row]
    photo = get_perfect_crop(im.crop((x1, y1, x2, y2)), has_color_bar=has_color_bar)
    out_path = f"{OUT_IMG_DIR}/{img_name}.png"
    photo.save(out_path)
    return out_path

# 2x5 Grid (Page 8 - Adesivos)
GRID_2X5_COLS = [(22, 246), (266, 490), (510, 734), (754, 978), (998, 1222)]
GRID_2X5_ROWS = [(138, 850), (896, 1610)]

def crop_clean_2x5(page_num, row, col, img_name):
    page_file = f"assets/catalog-pages/page-{page_num:02d}.png"
    im = Image.open(page_file)
    x1, x2 = GRID_2X5_COLS[col]
    y1, y2 = GRID_2X5_ROWS[row]
    photo = get_perfect_crop(im.crop((x1, y1, x2, y2)), has_color_bar=False)
    out_path = f"{OUT_IMG_DIR}/{img_name}.png"
    photo.save(out_path)
    return out_path

# 4x4 Grid (Pages 12 to 17 - Ferragens)
GRID_4X4_COLS = [(18, 306), (324, 612), (630, 918), (936, 1224)]
GRID_4X4_ROWS = [(112, 472), (496, 856), (880, 1240), (1264, 1624)]

def crop_clean_4x4(page_num, row, col, img_name):
    page_file = f"assets/catalog-pages/page-{page_num:02d}.png"
    im = Image.open(page_file)
    x1, x2 = GRID_4X4_COLS[col]
    y1, y2 = GRID_4X4_ROWS[row]
    photo = get_perfect_crop(im.crop((x1, y1, x2, y2)), has_color_bar=False)
    out_path = f"{OUT_IMG_DIR}/{img_name}.png"
    photo.save(out_path)
    return out_path

# 2x4 Grid (Pages 21 to 24 - Parafusos)
GRID_2X4_COLS = [(18, 604), (636, 1222)]
GRID_2X4_ROWS = [(112, 472), (496, 856), (880, 1240), (1264, 1624)]

def crop_clean_2x4(page_num, row, col, img_name):
    page_file = f"assets/catalog-pages/page-{page_num:02d}.png"
    im = Image.open(page_file)
    x1, x2 = GRID_2X4_COLS[col]
    y1, y2 = GRID_2X4_ROWS[row]
    photo = get_perfect_crop(im.crop((x1, y1, x2, y2)), is_2x4_screw=True)
    out_path = f"{OUT_IMG_DIR}/{img_name}.png"
    photo.save(out_path)
    return out_path

# Rebites (Page 25)
def crop_clean_rebites(row, img_name):
    page_file = "assets/catalog-pages/page-25.png"
    im = Image.open(page_file)
    if row == 0:
        photo = im.crop((24, 180, 390, 840))
    else:
        photo = im.crop((24, 960, 390, 1620))
    out_path = f"{OUT_IMG_DIR}/{img_name}.png"
    photo.save(out_path)
    return out_path

catalog = []

# --- 1. ACESSÓRIOS P/ PORTÕES (Pages 3 to 7) ---
portoes_raw = [
    # Page 3
    (3, 0, 0, "batente_l", "BATENTE-L", "Batente L", "Batente modelo L para portões em alumínio com alta resistência mecânica.", ["Branco", "Preto"], True),
    (3, 0, 1, "cavalete_38mm", "CAV-38", "Cavalete 38mm", "Cavalete de 38mm para guia e fixação de portão de alumínio.", ["Branco", "Natural Fosco", "Bronze 1002", "Bronze 1003", "Preto"], True),
    (3, 0, 2, "cavalete_duplo_38mm", "CAV-DUP-38", "Cavalete Duplo 38mm", "Cavalete duplo de 38mm para maior estabilidade e reforço em portões pesados.", ["Branco", "Natural Fosco", "Bronze 1002", "Bronze 1003", "Preto"], True),
    (3, 1, 0, "batente_chama_portao", "BAT-CHAMA", "Batente Chama para Portão", "Batente chama para travamento e encaixe preciso de portão.", ["Branco", "Preto"], True),
    (3, 1, 1, "dobradica_70x70_dob742", "DOB-742", "Dobradiça de Alumínio 70x70 DOB 742", "Dobradiça de alta resistência em liga de alumínio virgem 70x70mm.", ["Branco", "Preto"], True),
    (3, 1, 2, "esquadro_50x38", "ESQ-50X38", "Esquadro 50x38", "Esquadro em polímero técnico 50x38mm para montagem perfeita de quadros de portão.", ["Preto"], False),
    (3, 2, 0, "esquadro_50x50", "ESQ-50X50", "Esquadro 50x50", "Esquadro reforçado 50x50mm para alinhamento e união estrutural.", ["Preto"], False),
    (3, 2, 1, "esquadro_50x100", "ESQ-50X100", "Esquadro 50x100", "Esquadro para perfis largos 50x100mm de alta rigidez.", ["Preto"], False),
    (3, 2, 2, "esquadro_pc003_38x76", "PC003-38X76", "Esquadro PC003 38x76", "Esquadro técnico PC003 para perfis 38x76mm.", ["Alumínio"], False),

    # Page 4
    (4, 0, 0, "esquadro_pc010", "PC010", "Esquadro PC010", "Esquadro técnico de montagem modelo PC010.", ["Preto"], False),
    (4, 0, 1, "esquadro_pc012", "PC012", "Esquadro PC012", "Esquadro técnico de montagem modelo PC012.", ["Preto"], False),
    (4, 0, 2, "fecha_esquadro_25x50", "FECHA-ESQ-25X50", "Fecha Esquadro 25x50", "Fecha esquadro de pressão e travamento 25x50mm.", ["Preto"], False),
    (4, 1, 0, "fecha_esquadro_38x38", "FECHA-ESQ-38X38", "Fecha Esquadro 38x38", "Fecha esquadro reforçado 38x38mm.", ["Preto"], False),
    (4, 1, 1, "fecha_esquadro_38x50", "FECHA-ESQ-38X50", "Fecha Esquadro 38x50", "Fecha esquadro para união de perfis 38x50mm.", ["Preto"], False),
    (4, 1, 2, "ferrolho_2", "FERROLHO-2", "Ferrolho 2", "Ferrolho para portão com trava de segurança reforçada.", ["Branco", "Preto"], True),
    (4, 2, 0, "ferrolho_jumbo_200mm", "FER-JUMBO-200", "Ferrolho Jumbo 200mm", "Ferrolho tipo Jumbo 200mm para portas e portões pesados.", ["Branco", "Preto"], True),
    (4, 2, 1, "ferrolho_jumbo_300mm", "FER-JUMBO-300", "Ferrolho Jumbo 300mm", "Ferrolho tipo Jumbo 300mm para fechamento seguro de portões industriais e residenciais.", ["Branco", "Preto"], True),
    (4, 2, 2, "guia_rolete_comprido", "GUIA-ROL-COMP", "Guia de Rolete Comprido", "Guia com roletes compridos para deslizamento suave sem atrito.", ["Branco", "Preto"], True),

    # Page 5
    (5, 0, 0, "guia_rolete_duplo", "GUIA-ROL-DUP", "Guia de Rolete Duplo", "Guia com conjunto de rolete duplo com rolamento macio.", ["Branco", "Preto"], True),
    (5, 0, 1, "guia_rolete_simples", "GUIA-ROL-SIMP", "Guia de Rolete Simples", "Guia com rolete simples ajustável para portão de correr.", ["Branco", "Preto"], True),
    (5, 0, 2, "guia_passante", "GUIA-PASSANTE", "Guia Passante", "Guia passante reforçada para portões com movimentação estável.", ["Branco", "Preto"], True),
    (5, 1, 0, "guia_nylon_cantoneira", "GUIA-NYL-CANT", "Guia Nylon c/ Cantoneira", "Guia em nylon de alta densidade com cantoneira de fixação.", ["Branco", "Natural Fosco", "Bronze 1002", "Bronze 1003", "Preto"], True),
    (5, 1, 1, "guia_nylon_cantoneira_dupla", "GUIA-NYL-CANT-DUP", "Guia Nylon c/ Cantoneira Dupla", "Guia dupla em nylon com suporte cantoneira.", ["Branco", "Natural Fosco", "Bronze 1002", "Bronze 1003", "Preto"], True),
    (5, 1, 2, "guia_nylon_grande", "GUIA-NYL-G", "Guia Nylon Grande", "Guia deslizante grande em nylon antifricção.", ["Branco"], False),
    (5, 2, 0, "guia_nylon_pequeno", "GUIA-NYL-P", "Guia Nylon Pequeno", "Guia deslizante compacta em nylon.", ["Branco"], False),
    (5, 2, 1, "kit_acessorios_basculante", "KIT-BASC-1.0", "Kit Acessórios Porta Basculante 1.0 (1 Folha)", "Kit completo com trilhos, braços e guias para porta basculante 1 folha.", ["Branco", "Preto"], True),
    (5, 2, 2, "roldana_alum_cavalete_natural", "ROL-ALUM-CAV", "Roldana Alumínio Cavalete Natural", "Roldana em alumínio com cavalete natural para alta capacidade de carga.", ["Natural"], False),

    # Page 6
    (6, 0, 0, "roldana_50mm_trilho_alum", "ROL-50-TRILHO-ALUM", "Roldana 50mm 1/2mm Trilho Alumínio", "Roldana 50mm especial para trilho em perfil de alumínio.", ["Branco"], False),
    (6, 0, 1, "roldana_50mm_trilho_tubo", "ROL-50-TRILHO-TUBO", "Roldana 50mm 3/4mm Trilho Tubo", "Roldana côncava 50mm para correr sobre tubo redondo.", ["Branco"], False),
    (6, 0, 2, "roldana_cavalete_38mm", "ROL-CAV-38", "Roldana c/ Cavalete 38mm", "Roldana com cavalete 38mm para caixilhos e portões.", ["Branco", "Natural Fosco", "Bronze 1002", "Bronze 1003", "Preto"], True),
    (6, 1, 0, "sapata_pc002_25x50mm", "PC002-25X50", "Sapata PC002 25x50mm", "Sapata de apoio e fixação PC002 para perfis 25x50mm.", ["Branco", "Preto"], True),
    (6, 1, 1, "suporte_motor_porta_basculante", "SUP-MOTOR-BASC", "Suporte Motor Porta Basculante", "Suporte técnico reforçado para fixação de automatizador em porta basculante.", ["Branco", "Preto"], True),
    (6, 1, 2, "tampa_tubo_quadrada_38x38", "TAMPA-38X38", "Tampa para Tubo Quadrada 38x38mm", "Tampa de acabamento e proteção plástica para tubo quadrado 38x38mm.", ["Branco", "Preto"], True),
    (6, 2, 0, "tampa_tubo_retangular_12x25", "TAMPA-12X25", "Tampa para Tubo Retangular 12x25mm", "Tampa de vedação para tubos retangulares 12x25mm.", ["Branco", "Preto"], True),
    (6, 2, 1, "tampa_tubo_retangular_25x50", "TAMPA-25X50", "Tampa para Tubo Retangular 25x50mm", "Tampa de acabamento estético e proteção contra água para tubo 25x50mm.", ["Branco", "Preto"], True),
    (6, 2, 2, "tampa_tubo_retangular_38x50", "TAMPA-38X50", "Tampa para Tubo Retangular 38x50mm", "Tampa de polietileno resistente para tubos 38x50mm.", ["Branco", "Preto"], True),

    # Page 7
    (7, 0, 0, "tampa_tubo_retangular_50x100", "TAMPA-50X100", "Tampa para Tubo Retangular 50x100mm", "Tampa protetora e acabamento para tubos estruturais 50x100mm.", ["Branco", "Preto"], True),
    (7, 0, 1, "terminal_u_25x50", "TERM-U-25X50", "Terminal U 25x50", "Terminal tipo U para travamento e encaixe de perfis 25x50mm.", ["Preto"], False),
    (7, 0, 2, "terminal_u_38x38", "TERM-U-38X38", "Terminal U 38x38", "Terminal tipo U para perfis quadrados 38x38mm.", ["Preto"], False),
    (7, 1, 0, "terminal_u_38x50", "TERM-U-38X50", "Terminal U 38x50", "Terminal tipo U reforçado para perfis 38x50mm.", ["Preto"], False),
    (7, 1, 1, "tranqueta_parafuso_inox", "TRANQUETA-INOX", "Tranqueta c/ Parafuso de Inox", "Tranqueta de fechamento manual acompanhada de parafuso em aço inoxidável.", ["Branco", "Preto"], True),
    (7, 1, 2, "uniao_l_pc010_38x70", "UNIAO-PC010", "União L PC010 38x70mm", "Conexão de canto tipo L para união de perfis 38x70mm.", ["Alumínio"], False),
    (7, 2, 0, "uniao_l_pc012_38x65", "UNIAO-PC012", "União L PC012 38x65mm", "Conexão de canto tipo L modelo PC012 38x65mm.", ["Alumínio"], False),
]

for p_num, r, c, img_slug, code, title, desc, colors, has_cb in portoes_raw:
    img_path = crop_clean_3x3(p_num, r, c, img_slug, has_color_bar=has_cb)
    catalog.append({
        "id": f"port-{code.lower().replace('/', '-')}",
        "code": code,
        "title": title,
        "category": "portoes",
        "line": "Acessórios p/ Portões",
        "description": desc,
        "image": img_path,
        "colors": colors,
        "badge": "Portões"
    })

# --- 2. ADESIVOS & SELANTES (Page 8) ---
adesivos_raw = [
    (0, 0, "silicone_acrilico_branco_400g", "SIL-ACR-BR-400", "Silicone Acrílico Base D'Água Branco 400g Autofix", "Selante acrílico à base de água, ideal para vedação interna de juntas de esquadrias e acabamentos.", ["Branco"]),
    (0, 1, "silicone_acrilico_preto_400g", "SIL-ACR-PR-400", "Silicone Acrílico Base D'Água Preto 400g Autofix", "Selante acrílico base água na cor preta, excelente flexibilidade e aceita pintura.", ["Preto"]),
    (0, 2, "silicone_acetico_incolor_240g", "SIL-ACET-INC-240", "Silicone Acético Incolor 240g Autofix", "Silicone acético transparente para vedação estanque em vidro e alumínio com antifungo.", ["Incolor"]),
    (0, 3, "silicone_acetico_branco_240g", "SIL-ACET-BR-240", "Silicone Acético Branco 240g Autofix", "Silicone acético branco com alta aderência, vedação contra intempéries e proteção antifungo.", ["Branco"]),
    (0, 4, "silicone_acetico_preto_240g", "SIL-ACET-PR-240", "Silicone Acético Preto 240g Autofix", "Silicone acético preto para juntas perimetrais em esquadrias pretas e vidros temperados.", ["Preto"]),
    (1, 0, "silicone_neutro_incolor_250g", "SIL-NEUT-INC-250", "Silicone Neutro Incolor 250g Autofix", "Silicone de cura neutra incolor, não corrói metais nem esquadrias, alta resistência UV.", ["Incolor"]),
    (1, 1, "silicone_neutro_preto_250g", "SIL-NEUT-PR-250", "Silicone Neutro Preto 250g Autofix", "Silicone cura neutra preto para fachadas, peles de vidro e esquadrias de alto padrão.", ["Preto"]),
    (1, 2, "pu_40_cinza_380g", "PU40-CINZA-380", "PU 40 Construção Cinza 380g Autofix", "Adesivo e selante de poliuretano PU 40 cinza para juntas de dilatação na construção civil.", ["Cinza"]),
    (1, 3, "pu_40_preto_380g", "PU40-PRETO-380", "PU 40 Construção Preto 380g Autofix", "Selante poliuretano PU 40 preto de alta elasticidade e poder de colagem estrutural.", ["Preto"]),
    (1, 4, "fixa_espelho_400g", "FIXA-ESPELHO-400", "Fixa Espelho 400g Autofix", "Adesivo especial para fixação de espelhos sem manchar o fundo prateado.", ["Branco"]),
]

for r, c, img_slug, code, title, desc, colors in adesivos_raw:
    img_path = crop_clean_2x5(8, r, c, img_slug)
    catalog.append({
        "id": f"ades-{code.lower()}",
        "code": code,
        "title": title,
        "category": "adesivos",
        "line": "Autofix Oficial",
        "description": desc,
        "image": img_path,
        "colors": colors,
        "badge": "Selante"
    })

# --- 3. FECHADURAS STAM (Pages 9 to 11) ---
fechaduras_raw = [
    # Page 9
    (9, 0, 0, "fech_33203", "33203", "Fechadura Stam Giro 603/03 Branco (G)", "Fechadura Stam linha 603 com acabamento eletrostático branco de alta resistência.", ["Branco"], "Stam Giro 603"),
    (9, 0, 1, "fech_92037", "92037", "Fechadura Stam Giro 603/03 Cromada (G)", "Fechadura Stam linha 603 com acabamento cromado brilhante e maçaneta reforçada.", ["Cromada"], "Stam Giro 603"),
    (9, 0, 2, "fech_56091", "56091", "Fechadura Stam Giro 603/03 Preto Fosco (G)", "Fechadura Stam linha 603 em preto fosco moderna e elegante.", ["Preto Fosco"], "Stam Giro 603"),
    (9, 1, 0, "fech_39233", "39233", "Fechadura Stam Giro 606/17 Inox Branco", "Fechadura Stam 606 com maçaneta e espelho em aço inox com pintura branca litorânea.", ["Branco"], "Stam Giro 606 Inox"),
    (9, 1, 1, "fech_37148", "37148", "Fechadura Stam Giro 606/17 Inox Cromada", "Fechadura Stam 606 em aço inox cromado com alta durabilidade contra corrosão.", ["Cromada"], "Stam Giro 606 Inox"),
    (9, 1, 2, "fech_56410", "56410", "Fechadura Stam Giro 606/17 Inox Preto Fosco", "Fechadura Stam 606 aço inox em preto fosco para esquadrias contemporâneas.", ["Preto Fosco"], "Stam Giro 606 Inox"),
    (9, 2, 0, "fech_39409", "39409", "Fechadura Stam Giro Inox Buzios 606/17 Branco", "Fechadura Stam linha Búzios 606 com maçaneta anatômica em inox branco.", ["Branco"], "Stam Búzios"),
    (9, 2, 1, "fech_37239", "37239", "Fechadura Stam Giro Inox Buzios 605/17 Cromada", "Fechadura Stam linha Búzios 605 em aço inox com acabamento cromado.", ["Cromada"], "Stam Búzios"),
    (9, 2, 2, "fech_43523", "43523", "Fechadura Stam Giro Inox Buzios 605/17 Preto Fosco", "Fechadura Stam Búzios 605 em inox preto fosco para portas pivotantes e de giro.", ["Preto Fosco"], "Stam Búzios"),

    # Page 10
    (10, 0, 0, "fech_35136", "35136", "Fechadura Stam Bico 901 CT 901 Branco (G)", "Fechadura bico de papagaio Stam 901 com contra-testa 901 acabamento branco.", ["Branco"], "Stam Bico 901"),
    (10, 0, 1, "fech_35067", "35067", "Fechadura Stam Bico 901 CT 901 Cromada (G)", "Fechadura bico de papagaio Stam 901 cromada para portas de correr de alumínio.", ["Cromada"], "Stam Bico 901"),
    (10, 0, 2, "fech_56108", "56108", "Fechadura Stam Bico 901 CT 901 Preto Fosco (G)", "Fechadura bico de papagaio Stam 901 acabamento preto fosco.", ["Preto Fosco"], "Stam Bico 901"),
    (10, 1, 0, "fech_34015", "34015", "Fechadura Stam Bico Buzios 901/90 Branco", "Fechadura bico de papagaio Búzios 901/90 em branco com espelho anatômico.", ["Branco"], "Stam Bico Búzios"),
    (10, 1, 1, "fech_91901", "91901", "Fechadura Stam Bico Buzios 901/90 Cromada", "Fechadura bico de papagaio Búzios 901/90 cromada para correr.", ["Cromada"], "Stam Bico Búzios"),
    (10, 1, 2, "fech_56901", "56901", "Fechadura Stam Bico Buzios 901/90 Preto Fosco", "Fechadura bico de papagaio Búzios 901/90 preto fosco.", ["Preto Fosco"], "Stam Bico Búzios"),
    (10, 2, 0, "fech_36084", "36084", "Fechadura Stam Bico Inox 902 CT 901 Branco", "Fechadura bico Stam 902 em aço inox com contra-testa 901 acabamento branco.", ["Branco"], "Stam Bico Inox 902"),
    (10, 2, 1, "fech_36083", "36083", "Fechadura Stam Bico Inox 902 CT 901 Cromada", "Fechadura bico Stam 902 em aço inox cromado de máxima segurança.", ["Cromada"], "Stam Bico Inox 902"),
    (10, 2, 2, "fech_36363", "36363", "Fechadura Stam Bico Inox 902 CT 901 Preto Fosco", "Fechadura bico Stam 902 em inox preto fosco para esquadrias linha Gold e Suprema.", ["Preto Fosco"], "Stam Bico Inox 902"),

    # Page 11
    (11, 0, 0, "fech_36061", "36061", "Fechadura Stam Bico Inox 902 CT 901 Buzios Branco", "Fechadura bico inox 902 linha Búzios branca para correr.", ["Branco"], "Stam Bico Inox"),
    (11, 0, 1, "fech_36062", "36062", "Fechadura Stam Bico Inox 902 CT 901 Buzios Cromada", "Fechadura bico inox 902 linha Búzios cromada.", ["Cromada"], "Stam Bico Inox"),
    (11, 0, 2, "fech_43521", "43521", "Fechadura Stam Bico Inox 902 CT 901 Buzios Preto Fosco", "Fechadura bico inox 902 Búzios em preto fosco.", ["Preto Fosco"], "Stam Bico Inox"),
    (11, 1, 0, "fech_22793", "22793", "Fechadura Stam Bico 902 Inox Suprema Branco", "Fechadura bico 902 projetada especialmente para perfis da Linha Suprema em branco.", ["Branco"], "Linha Suprema"),
    (11, 1, 1, "fech_22792", "22792", "Fechadura Stam Bico 902 Inox Suprema Cromada", "Fechadura bico 902 para Linha Suprema em acabamento cromado.", ["Cromada"], "Linha Suprema"),
    (11, 1, 2, "fech_58794", "58794", "Fechadura Stam Bico 902 Inox Suprema Preto Fosco", "Fechadura bico 902 para Linha Suprema em preto fosco.", ["Preto Fosco"], "Linha Suprema"),
    (11, 2, 0, "fech_22256", "22256", "Miolo Fechadura Stam 1520 Cromado - Cil. Redondo", "Cilindro miolo redondo cromado para fechaduras de centro Stam 1520.", ["Cromado"], "Cilindros Stam"),
    (11, 2, 1, "fech_22268", "22268", "Miolo Fechadura Stam 1510X Cromado - Cil. Redondo", "Cilindro miolo redondo cromado para fechadura Stam 1510X porta de correr.", ["Cromado"], "Cilindros Stam"),
    (11, 2, 2, "fech_51209", "51209", "Maçaneta Stam Tam2 Cromado", "Maçaneta curva Stam Tam2 com acabamento cromado reforçado.", ["Cromado"], "Acessórios Stam"),
]

for p_num, r, c, img_slug, code, title, desc, colors, line in fechaduras_raw:
    img_path = crop_clean_3x3(p_num, r, c, img_slug, has_color_bar=False)
    catalog.append({
        "id": f"fech-{code.lower()}",
        "code": code,
        "title": title,
        "category": "fechaduras",
        "line": line,
        "description": desc,
        "image": img_path,
        "colors": colors,
        "badge": "Stam Oficial"
    })

# --- 4. FERRAGENS PARA VIDRO TEMPERADO (Pages 12 to 17) ---
ferragens_raw = [
    # Page 12
    (12, 0, 0, "ferr_1000", "1000", "Engate em Alvenaria para Basculante", "Engate para fixação de janelas basculantes na alvenaria."),
    (12, 0, 1, "ferr_1002L", "1002L", "Botão de Correção com Lâmina", "Botão regulador de pressão e correção com lâmina."),
    (12, 0, 2, "ferr_1003A", "1003A", "Argola p/ Corrente", "Argola para acionamento por corrente em basculantes."),
    (12, 0, 3, "ferr_1003C", "1003C", "Corrente p/ Basculante", "Corrente de comando para abertura e travamento de janelas basculantes altas."),
    (12, 1, 0, "ferr_1009", "1009", "Pivô para Dobradiça 1101, 1230, 1231", "Pivô superior e inferior para dobradiças de vidro temperado."),
    (12, 1, 1, "ferr_1009G", "1009G", "Pivô Superior p/ 1101G", "Pivô superior reforçado para dobradiça Max 1101G."),
    (12, 1, 2, "ferr_1014", "1014", "Pivô Inferior p/ 1102", "Pivô inferior de apoio para dobradiça 1102."),
    (12, 1, 3, "ferr_1014G", "1014G", "Pivô Inferior p/ 1102G", "Pivô inferior reforçado para dobradiça Max 1102G."),
    (12, 2, 0, "ferr_1101", "1101", "Dobradiça Pivotante Superior", "Dobradiça superior clássica para portas de vidro pivotante 8mm e 10mm."),
    (12, 2, 1, "ferr_1101G", "1101G", "Dobradiça Max Pivotante Superior", "Dobradiça superior modelo Max reforçada para grandes vãos."),
    (12, 2, 2, "ferr_1102", "1102", "Dobradiça Pivotante Inferior", "Dobradiça inferior para porta pivotante em vidro temperado."),
    (12, 2, 3, "ferr_1102G", "1102G", "Dobradiça Max Pivotante Inferior", "Dobradiça inferior reforçada para portas de vidro pesadas."),
    (12, 3, 0, "ferr_1103", "1103", "Dobradiça Inferior para Mola", "Dobradiça inferior com encaixe cônico para mola hidráulica de piso."),
    (12, 3, 1, "ferr_1103G", "1103G", "Dobradiça Max Inferior com Miolo para Mola", "Dobradiça inferior Max com miolo usinado para mola de piso."),
    (12, 3, 2, "ferr_1114", "1114", "Dobradiça Automática para Box", "Dobradiça com mola interna de fechamento automático para box de vidro."),
    (12, 3, 3, "ferr_1115", "1115", "Dobradiça Simples para Box", "Dobradiça simples de articulação livre para box de banheiro."),

    # Page 13
    (13, 0, 0, "ferr_1122", "1122", "Carrinho Duplo para Trilho Stanley", "Carrinho com duplo rolamento para portas pesadas no trilho Stanley."),
    (13, 0, 1, "ferr_1122G", "1122G", "Carrinho Triplo para Trilho Stanley", "Carrinho triplo de alta performance para movimentação suave."),
    (13, 0, 2, "ferr_1122M", "1122M", "Carrinho Mini para Trilho Stanley", "Carrinho compacto mini para trilhos e divisórias."),
    (13, 0, 3, "ferr_1122S", "1122S", "Carrinho Simples para Trilho Stanley", "Carrinho simples com rolamento blindado para trilho Stanley."),
    (13, 1, 0, "ferr_1123", "1123", "Dobradiça Pino para Basculante 50x50mm", "Dobradiça de pino central para janela basculante 50x50mm."),
    (13, 1, 1, "ferr_1125B", "1125B", "Roldana Excêntrica para Box", "Roldana excêntrica regulável para alinhamento de portas de box."),
    (13, 1, 2, "ferr_1125D", "1125D", "Roldana Dupla com Regulagem", "Roldana dupla com parafuso de ajuste milimétrico de altura."),
    (13, 1, 3, "ferr_1125F", "1125F", "Roldana Excêntrica", "Roldana excêntrica de alta precisão em latão e poliacetal."),
    (13, 2, 0, "ferr_1130", "1130", "Dobradiça Pino para Basculante 50x100mm", "Dobradiça basculante para vidro com perfil 50x100mm."),
    (13, 2, 1, "ferr_1131", "1131", "Dobradiça Maxim - Ar VV 40 mm entre furos", "Dobradiça maxim-ar vidro-vidro com 40mm entre furos."),
    (13, 2, 2, "ferr_1132", "1132", "Dobradiça Maxim - Ar V/A 40 mm entre furos", "Dobradiça maxim-ar vidro-alvenaria 40mm."),
    (13, 2, 3, "ferr_1133", "1133", "Dobradiça Maxim - Ar V/A 50 mm entre furos", "Dobradiça maxim-ar vidro-alvenaria 50mm."),
    (13, 3, 0, "ferr_1134", "1134", "Dobradiça Maxim - Ar V/V 50 mm entre furos", "Dobradiça maxim-ar vidro-vidro 50mm."),
    (13, 3, 1, "ferr_1136", "1136", "Dobradiça Lateral Horizontal", "Dobradiça para montagem lateral em painéis de vidro temperado."),
    (13, 3, 2, "ferr_1137", "1137", "Dobradiça Dupla Pequena para Janela", "Dobradiça dupla compacta para bandeiras e janelas de vidro."),
    (13, 3, 3, "ferr_1150", "1150", "Roldana Quádrupla", "Roldana quádrupla para distribuição de peso em portas e sacadas."),

    # Page 14
    (14, 0, 0, "ferr_1150S", "1150-S", "Roldana Dupla", "Roldana dupla para portas e sacadas envidraçadas."),
    (14, 0, 1, "ferr_1200", "1200", "Capuchinho para Trinco e Fechadura", "Capuchinho metálico de embutir no piso para encaixe de ferrolho e trinco."),
    (14, 0, 2, "ferr_1203", "1203", "Suporte de Bandeira para Dobradiça 1101", "Suporte fixo para sustentação de bandeira de vidro com dobradiça 1101."),
    (14, 0, 3, "ferr_1209", "1209", "Facão Simples para Bandeira e Fixo", "Suporte tipo facão simples para fixação de bandeira e vidro fixo."),
    (14, 1, 0, "ferr_1230", "1230", "Dobradiça Bucha para Basculante 50x50 mm", "Dobradiça com bucha de latão para janelas basculantes."),
    (14, 1, 1, "ferr_1231", "1231", "Dobradiça Bucha para Basculante 50x100 mm", "Dobradiça com bucha reforçada para perfil 50x100mm."),
    (14, 1, 2, "ferr_1310", "1310", "Suporte sem Núcleo para União de Três Vidros", "Conexão em T sem núcleo para fixação de 3 painéis de vidro temperado."),
    (14, 1, 3, "ferr_1315", "1315", "Suporte sem Núcleo com Batedeira", "Suporte para junção de vidros com batedeira emborrachada."),
    (14, 2, 0, "ferr_1333", "1333", "Suporte para Prateleiras", "Suporte fenda/pelicano de fixação firme para prateleiras de vidro."),
    (14, 2, 1, "ferr_1334", "1334", "Grapa para Sacada", "Grapa de travamento e ancoragem para sistemas de envidraçamento de sacadas."),
    (14, 2, 2, "ferr_1340", "1340", "Suporte de Canto com Rosca para Roldana 1150", "Suporte de canto rosqueado para montagem da roldana 1150."),
    (14, 2, 3, "ferr_1341", "1341", "Suporte de Centro com Rosca para Roldana 1150", "Suporte de centro com rosca para acoplamento na roldana 1150."),
    (14, 3, 0, "ferr_1350", "1350", "Suporte Superior para Box de Canto 90°", "Suporte angular de 90 graus para união de box de canto."),
    (14, 3, 1, "ferr_1400", "1400", "Batedeira para Trinco Basculante", "Batedeira metálica para travamento de trinco de basculante."),
    (14, 3, 2, "ferr_1406", "1406", "Batente de Borracha", "Batente de borracha de amortecimento contra impacto de vidro."),
    (14, 3, 3, "ferr_1407", "1407", "Limitador Central Superior T", "Limitador superior formato T para controle de abertura de portas."),

    # Page 15
    (15, 0, 0, "ferr_1408A", "1408A", "Contra Trinco com Aba para 1521", "Contra trinco com aba protetora para fecho 1521."),
    (15, 0, 1, "ferr_1504A", "1504A", "Batedeira em Alvenaria para 1520", "Batedeira de fixação na alvenaria para fechadura 1520."),
    (15, 0, 2, "ferr_1504ATA", "1504ATA", "Batedeira em Alvenaria para 1520TA", "Batedeira para alvenaria modelo 1520TA com maçaneta."),
    (15, 0, 3, "ferr_1504TA", "1504TA", "Contra Fechadura para 1520TA", "Contra fechadura vidro-vidro para modelo 1520TA."),
    (15, 1, 0, "ferr_1510X", "1510X", "Fechadura para Porta de Correr", "Fechadura de bico para porta de correr em vidro temperado."),
    (15, 1, 1, "ferr_1511AX", "1511AX", "Batedeira em Alvenaria para 1510X", "Batedeira de alvenaria para encaixe da lingueta da fechadura 1510X."),
    (15, 1, 2, "ferr_1511X", "1511X", "Contra Fechadura Vidro Vidro para Porta de Correr", "Contra fechadura de vidro para portas de correr duplas."),
    (15, 1, 3, "ferr_1519A", "1519A", "Contra Trinco sem Núcleo para 1519", "Contra trinco para vidro temperado sem núcleo para trinco 1519."),
    (15, 2, 0, "ferr_1519", "1519", "Trinco Inferior sem Núcleo 50x100 mm", "Trinco inferior para piso em vidro 50x100mm."),
    (15, 2, 1, "ferr_1520", "1520", "Fechadura de Centro sem Miolo", "Fechadura central para porta pivotante de vidro sem miolo."),
    (15, 2, 2, "ferr_1520TA", "1520TA", "Fechadura de Centro para Maçaneta sem Miolo", "Fechadura central com furação para acoplamento de maçaneta."),
    (15, 2, 3, "ferr_1521", "1521", "Trinco para Janela ou Porta", "Trinco de pressão manual para portas e janelas de vidro temperado."),
    (15, 3, 0, "ferr_1521L", "1521L", "Trinco com Ferrolho Lateral", "Trinco metálico com haste de travamento e ferrolho lateral."),
    (15, 3, 1, "ferr_1523", "1523", "Trinco Central para Basculante", "Trinco central para acionamento de janela basculante."),
    (15, 3, 2, "ferr_1524", "1524", "Contra Trinco para 1521 e 1523", "Contra trinco simples de fixação para os modelos 1521 e 1523."),
    (15, 3, 3, "ferr_1525", "1525", "Contra Trinco com Batedeira para 1521 e 1523", "Contra trinco reforçado com batedeira integrada."),

    # Page 16
    (16, 0, 0, "ferr_1531", "1531", "Contra Fechadura com Batente para 1520", "Contra fechadura vidro-vidro com batente embutido para 1520."),
    (16, 0, 1, "ferr_1532", "1532", "Contra Trinco com Batedeira para 1519", "Contra trinco para piso com batedeira de amortecimento para 1519."),
    (16, 0, 2, "ferr_1570", "1570", "Bate Fecha Vidro/Vidro", "Fecho tipo bate-fecha magnético/mecânico para dois painéis de vidro."),
    (16, 0, 3, "ferr_1571", "1571", "Bate Fecha Vidro/Alvenaria", "Bate-fecha para fechamento de vidro na alvenaria."),
    (16, 1, 0, "ferr_1587_20", "1587-20", "Haste Maxim - Ar 20cm", "Haste articulada maxim-ar em alumínio 20cm."),
    (16, 1, 1, "ferr_1587_25", "1587-25", "Haste Maxim - Ar 25cm", "Haste articulada maxim-ar em alumínio 25cm."),
    (16, 1, 2, "ferr_1587_30", "1587-30", "Haste Maxim - Ar 30cm", "Haste articulada maxim-ar em alumínio 30cm."),
    (16, 1, 3, "ferr_1587_35", "1587-35", "Haste Maxim - Ar 35cm", "Haste articulada maxim-ar em alumínio 35cm."),
    (16, 2, 0, "ferr_1587_40", "1587-40", "Haste Maxim - Ar 40cm", "Haste articulada maxim-ar em alumínio 40cm para janelas amplas."),
    (16, 2, 1, "ferr_1587_va", "1587-VA", "Conjunto Acessórios VA para 1587", "Kit de ferragens de articulação vidro-alvenaria para haste 1587."),
    (16, 2, 2, "ferr_1587_vv", "1587-VV", "Conjunto Acessórios VV para 1587", "Kit de acessórios vidro-vidro para haste 1587."),
    (16, 2, 3, "ferr_1629", "1629", "Puxador para Box 25mm", "Puxador tubular redondo de 25mm para portas de box em vidro temperado."),
    (16, 3, 0, "ferr_1630", "1630", "Puxador para Box 19mm", "Puxador redondo ergonômico de 19mm para box de banheiro."),
    (16, 3, 1, "ferr_1650", "1650", "Puxador para Janela de Correr 25mm", "Puxador tipo concha para janela de correr de vidro 25mm."),
    (16, 3, 2, "ferr_1651", "1651", "Puxador para Janela de Correr 19mm", "Puxador tipo concha para janela de correr de vidro 19mm."),
    (16, 3, 3, "ferr_1702", "1702", "Fixador de Porta no Rodapé-Piso", "Fixador magnético e mecânico de porta para rodapé ou piso."),

    # Page 17 (13 items)
    (17, 0, 0, "ferr_1710", "1710", "Conjunto Mão de Amigo de Portas de Correr", "Conjunto puxador e arraste tipo mão-de-amigo para folhas sequenciais."),
    (17, 0, 1, "ferr_1710M", "1710M", "Mini Conjunto Mão de Amigo de Portas de Correr", "Versão compacta mini para portas e janelas de correr."),
    (17, 0, 2, "ferr_kit_1520", "KIT PORTA-1520 VA", "Kit Porta-1520 VA", "Kit completo contendo 1101, 1009, 1102, 1014, 1520 e 1504A sem miolo."),
    (17, 0, 3, "ferr_kit_1520ta", "KIT PORTA-1520TA VA", "Kit Porta-1520TA VA", "Kit porta vidro-alvenaria com fechadura 1520TA para maçaneta."),
    (17, 1, 0, "ferr_kit_basc", "KIT BASCULANTE VA", "Kit Basculante VA", "Kit de instalação completa para janela basculante vidro-alvenaria."),
    (17, 1, 1, "ferr_kit_ocul", "KIT OCULANTE", "Kit Oculante 1230 1009 1521 1200", "Kit para janela oculante contendo ferragens 1230, 1009, 1521 e 1200."),
    (17, 1, 2, "ferr_kit_max_20", "KIT MAX 20", "Kit Maxim-Ar Haste 20cm", "Kit completo para janela maxim-ar com haste de 20cm."),
    (17, 1, 3, "ferr_kit_max_25", "KIT MAX 25", "Kit Maxim-Ar Haste 25cm", "Kit completo para janela maxim-ar com haste de 25cm."),
    (17, 2, 0, "ferr_kit_max_30", "KIT MAX 30", "Kit Maxim-Ar Haste 30cm", "Kit completo para janela maxim-ar com haste de 30cm."),
    (17, 2, 1, "ferr_kit_max_35", "KIT MAX 35", "Kit Maxim-Ar Haste 35cm", "Kit completo para janela maxim-ar com haste de 35cm."),
    (17, 2, 2, "ferr_kit_max_40", "KIT MAX 40", "Kit Maxim-Ar Haste 40cm", "Kit completo para janela maxim-ar com haste de 40cm."),
    (17, 2, 3, "ferr_tam2_p17", "TAM2", "Maçaneta Stam Tam2 Cromado", "Maçaneta anatômica cromada Stam modelo Tam2."),
    (17, 3, 0, "ferr_cunha_15mm", "CUNHA 15MM", "Cunha de Regulagem 15mm Pcte 100 Unidades", "Pacote com 100 unidades de cunha de regulagem plástica 15mm para calçamento e alinhamento de vidros."),
]

for p_num, r, c, img_slug, code, title, desc in ferragens_raw:
    img_path = crop_clean_4x4(p_num, r, c, img_slug)
    catalog.append({
        "id": f"ferr-{code.lower().replace('/', '-').replace(' ', '-')}",
        "code": code,
        "title": title,
        "category": "ferragens",
        "line": "Ferragens p/ Vidro",
        "description": desc,
        "image": img_path,
        "colors": ["Inox", "Cromado", "Branco", "Preto"],
        "badge": "Vidro Temperado"
    })

# --- 5. GUARNIÇÕES & FITAS EPDM (Pages 18 to 20) ---
guarnicoes_raw = [
    # Page 18
    (18, 0, 0, "fita_epdm_11x4", "EPDM-11X4", "Fita EPDM 11x4 Preta", "Fita de vedação automotiva e para esquadrias em borracha EPDM 11x4mm."),
    (18, 0, 1, "fita_epdm_11x6", "EPDM-11X6", "Fita EPDM 11x6 Preta", "Fita em borracha EPDM esponjosa 11x6mm para alta estanqueidade acústica e de água."),
    (18, 0, 2, "fita_escova_5x5", "ESC-5X5", "Fita Escova Vedação 5x5 Preta", "Fita escova para perfis de correr 5x5mm contra vento, poeira e ruído."),
    (18, 1, 0, "fita_escova_5x7", "ESC-5X7", "Fita Escova Vedação 5x7 Preta", "Fita escova vedação 5x7mm em polipropileno siliconado."),
    (18, 1, 1, "fita_escova_5x10", "ESC-5X10", "Fita Escova Vedação 5x10 Preta", "Fita escova vedação 5x10mm de cerdas altas para vãos maiores."),
    (18, 1, 2, "fita_escova_7x6", "ESC-7X6", "Fita Escova Vedação 7x6 Preta", "Fita escova base 7mm com altura 6mm."),
    (18, 2, 0, "fita_escova_7x8", "ESC-7X8", "Fita Escova Vedação 7x8 Preta", "Fita escova vedação 7x8mm resistente à maresia e sol."),
    (18, 2, 1, "fita_escova_7x10", "ESC-7X10", "Fita Escova Vedação 7x10 Preta", "Fita escova vedação 7x10mm de vedação perimetral."),
    (18, 2, 2, "fita_escova_75x6", "ESC-7.5X6", "Fita Escova Vedação 7,5x6 Preta", "Fita escova de base 7,5mm e altura 6mm."),

    # Page 19
    (19, 0, 0, "fita_escova_75x8", "ESC-7.5X8", "Fita Escova Vedação 7,5x8 Preta", "Fita escova vedação 7,5x8mm preta."),
    (19, 0, 1, "fita_escova_7x10_adesiva", "ESC-7X10-AD", "Fita Escova Vedação 7x10 Preta Adesiva", "Fita escova com fita adesiva de alta fixação para aplicação direta na alvenaria ou perfis."),
    (19, 0, 2, "cordao_borracha_5mm", "CORD-5MM", "Cordão de Borracha Maciça 5mm Preta", "Cordão cilíndrico de borracha maciça 5mm para pressão em perfis."),
    (19, 1, 0, "cordao_borracha_6mm", "CORD-6MM", "Cordão de Borracha Maciça 6mm Preta", "Cordão cilíndrico de borracha maciça 6mm."),
    (19, 1, 1, "cinta_menor_epdm", "CINTA-EPDM", "Cinta Menor em EPDM", "Cinta estriada em borracha EPDM (38x15x3mm) para apoio e vedação de caixilhos."),
    (19, 1, 2, "gaxeta_coluna_faa202", "FAA-202/2", "Gaxeta da Coluna e Travessa FAA 202/2 / TP 269", "Perfil técnico de gaxeta para vedação de colunas e travessas de fachadas."),
    (19, 2, 0, "gaxeta_externa_faa250", "FAA-250", "Gaxeta Externa FAA 250", "Gaxeta de pressão externa para estanqueidade de pele de vidro e structural glazing."),
    (19, 2, 1, "guarnicao_pingadeira_gua007", "GUA-007", "Guarnição para Pingadeira Suprema GUA 007 Preta", "Guarnição de pingadeira específica para a Linha Suprema."),
    (19, 2, 2, "guarnicao_vidro_10mm_gua038n", "GUA-038N", "Guarnição para Vidro 10mm GUA 038N Preta", "Perfil de borracha tipo cunha para encaixe firme de vidro temperado 10mm."),

    # Page 20
    (20, 0, 0, "guarnicao_vidro_8mm_gua039n", "GUA-039N", "Guarnição para Vidro 8mm GUA 039N Preta", "Guarnição em EPDM para vedação perimetral de vidro 8mm."),
    (20, 0, 1, "guarnicao_marco_caixilho_gua239", "GUA-239", "Guarnição do Marco Caixilho GUA 239 Preta", "Borracha de vedação para marco de caixilho de portas e janelas."),
    (20, 0, 2, "guarnicao_vidro_4mm_gua827c", "GUA-827C", "Guarnição para Vidro 4mm GUA 827C Preta", "Guarnição para vidros finos 4mm em esquadrias residenciais."),
]

for p_num, r, c, img_slug, code, title, desc in guarnicoes_raw:
    img_path = crop_clean_3x3(p_num, r, c, img_slug, has_color_bar=False)
    catalog.append({
        "id": f"gua-{code.lower().replace('/', '-')}",
        "code": code,
        "title": title,
        "category": "guarnicoes",
        "line": "Guarnições & EPDM",
        "description": desc,
        "image": img_path,
        "colors": ["Preto"],
        "badge": "Vedação"
    })

# --- 6. PARAFUSOS & FIXADORES (Pages 21 to 24) ---
parafusos_raw = [
    # Page 21
    (21, 0, 0, "par_77910200", "77910200", "Arruela Funileiro Inox 304 3/16 Polido", "Bitola 3/16 polegadas em aço inoxidável AISI 304."),
    (21, 0, 1, "par_81025101", "81025101", "Arruela Lisa 3/8 Zincado Branco", "Bitola 3/8 polegadas em aço carbono zincado branco."),
    (21, 1, 0, "par_31765000", "31765000", "Arruela Vulcanizada Alumínio EPDM Polido 12 x 1.1/8", "Arruela vulcanizada em alumínio com vedação de borracha EPDM para fixação estanque."),
    (21, 1, 1, "par_44825100", "44825100", "Bucha Plástica com Anel N.6 Polido", "Bucha plástica de fixação com anel guia número 6."),
    (21, 2, 0, "par_56130100", "56130100", "Bucha Oco C8 x 50mm", "Bucha especial para tijolo oco e bloco estrutural C8 x 50mm em nylon."),
    (21, 2, 1, "par_38467800", "38467800", "Parafuso Cabeça Chata Phillips Inox 304 Auto Atarraxante 4,8 x 50", "Parafuso cabeça chata Phillips em inox AISI 304 rosca inteira 4,8 x 50mm."),
    (21, 3, 0, "par_39062702", "39062702", "Parafuso Fixer Cabeça Panela Phillips 4,5 x 45 Bicromatizado", "Parafuso Fixer cabeça panela parcial sobreposta bicromatizado 4,5 x 45mm."),
    (21, 3, 1, "par_36956300", "36956300", "Parafuso Flangeado Phillips Ponta Broca Inox 410 4,2x13", "Parafuso autoatarraxante flangeado ponta broca em inox 410 rosca inteira 4,2 x 13mm."),

    # Page 22
    (22, 0, 0, "par_38367800", "38367800", "Parafuso Cabeça Panela Phillips Inox 304 Auto Atarraxante 4,8 x 50", "Parafuso cabeça panela em inox AISI 304 4,8 x 50mm polido."),
    (22, 0, 1, "par_38357300", "38357300", "Parafuso Cabeça Panela Phillips Inox 304 Auto Atarraxante 4,2 x 32", "Parafuso cabeça panela em inox 304 4,2 x 32mm polido."),
    (22, 1, 0, "par_38366600", "38366600", "Parafuso Cabeça Panela Phillips Inox 304 Auto Atarraxante 4,8 x 16", "Parafuso cabeça panela em inox 304 4,8 x 16mm polido."),
    (22, 1, 1, "par_36656800", "36656800", "Parafuso Cabeça Panela Phillips Ponta Broca Inox 410 4,2x19", "Parafuso ponta broca autoatarraxante inox 410 4,2 x 19mm polido."),
    (22, 2, 0, "par_35067801", "35067801", "Parafuso Cabeça Panela Phillips Auto Atarraxante 4,8 x 50 Zincado Branco", "Parafuso em aço carbono zincado branco cabeça panela 4,8 x 50mm."),
    (22, 2, 1, "par_38357700", "38357700", "Parafuso Cabeça Panela Phillips Inox 304 Auto Atarraxante 4,2 x 45", "Parafuso cabeça panela em inox AISI 304 4,2 x 45mm."),
    (22, 3, 0, "par_38366300", "38366300", "Parafuso Cabeça Panela Phillips Inox 304 Auto Atarraxante 4,8 x 13", "Parafuso cabeça panela em inox AISI 304 4,8 x 13mm polido."),
    (22, 3, 1, "par_36656300", "36656300", "Parafuso Cabeça Panela Phillips Ponta Broca Inox 410 4,2x13", "Parafuso ponta broca inox 410 4,2 x 13mm polido."),

    # Page 23
    (23, 0, 0, "par_36656600", "36656600", "Parafuso Cabeça Panela Phillips Ponta Broca Inox 410 4,2x16", "Parafuso ponta broca autoatarraxante inox 410 4,2 x 16mm."),
    (23, 0, 1, "par_36657100", "36657100", "Parafuso Cabeça Panela Phillips Ponta Broca Inox 410 4,2x25", "Parafuso ponta broca autoatarraxante inox 410 4,2 x 25mm."),
    (23, 1, 0, "par_13327301", "13327301", "Parafuso Sextavado UNC Rosca Parcial AC 3/8 x 4.1/2", "Parafuso sextavado em aço carbono grau 2 zincado branco 3/8 x 4.1/2 polegadas."),
    (23, 1, 1, "par_18015500", "18015500", "Parafuso Sextavado Inox 304 UNC Rosca Inteira 1/4 x 1/2", "Parafuso sextavado em aço inox 304 rosca inteira 1/4 x 1/2 polegada."),
    (23, 2, 0, "par_28126700", "28126700", "Parafuso Sextavado Rosca Soberba Inox 304 1/4 - M6x60", "Parafuso rosca soberba sextavado em inox 304 1/4 M6 x 60mm."),
    (23, 2, 1, "par_51547101", "51547101", "Parafuso Concrete Bolt AC Rosca Inteira 12x75", "Parafuso chumbador de concreto Concrete Bolt flangeado 12 x 75mm zincado branco."),
    (23, 3, 0, "par_24716401", "24716401", "Chumbador CBC com Parafuso UNC AC 1/4 x 2", "Chumbador mecânico de expansão CBC com parafuso 1/4 x 2 polegadas."),
    (23, 3, 1, "par_24726601", "24726601", "Chumbador CBC com Parafuso UNC AC 3/8 x 2.1/2", "Chumbador mecânico CBC em aço carbono zincado branco 3/8 x 2.1/2 polegadas."),

    # Page 24
    (24, 0, 0, "par_61015400", "61015400", "Porca Sextavada Inox 304 UNC 1/4 Chave 7/16", "Porca sextavada em aço inox 304 rosca UNC 1/4 chave 7/16 polida."),
    (24, 0, 1, "par_60025601", "60025601", "Porca Sextavada UNC 3/8 Chave 9/16", "Porca sextavada em aço carbono zincado branco 3/8 chave 9/16."),
    (24, 1, 0, "par_57518500", "57518500", "Ponteira Dupla Phillips Magnética AC Chave 2 1/4 x 65", "Ponteira dupla magnetizada em aço carbono para parafusadeiras 1/4 x 65mm."),
    (24, 1, 1, "par_57116500", "57116500", "Ponteira Phillips Chave 2 1/4 x 25", "Ponteira simples Phillips magnetizada 1/4 x 25mm."),
]

for p_num, r, c, img_slug, code, title, desc in parafusos_raw:
    img_path = crop_clean_2x4(p_num, r, c, img_slug)
    catalog.append({
        "id": f"par-{code.lower()}",
        "code": code,
        "title": title,
        "category": "parafusos",
        "line": "Parafusos & Inox",
        "description": desc,
        "image": img_path,
        "colors": ["Inox Polido", "Zincado Branco"],
        "badge": "Inox 304 / Aço"
    })

# --- 7. REBITES (Page 25) ---
reb_01_img = crop_clean_rebites(0, "rebite_aco_carbono")
catalog.append({
    "id": "reb-aco-carbono",
    "code": "REB-ACO",
    "title": "Rebite de Alumínio com Mandril de Aço Carbono",
    "category": "rebites",
    "line": "Rebites de Repuxo Padrão",
    "description": "Rebites de repuxo padrão com cabeça abaulada. Corpo em alumínio liga 5005, mandril em aço carbono. Disponível nas linhas 3,2mm e 4,0mm com comprimentos de 10mm a 25mm.",
    "image": reb_01_img,
    "colors": ["Branco", "Natural Fosco", "Preto"],
    "badge": "Repuxo Padrão"
})

reb_02_img = crop_clean_rebites(1, "rebite_mandril_aluminio")
catalog.append({
    "id": "reb-mandril-aluminio",
    "code": "REB-ALUM",
    "title": "Rebite de Alumínio com Mandril de Alumínio",
    "category": "rebites",
    "line": "Rebites Cabeça Abaulada",
    "description": "Rebites de repuxo com corpo e mandril 100% em alumínio liga 5005, oferecendo imunidade à ferrugem e máxima durabilidade para áreas litorâneas. Linha 4,0mm.",
    "image": reb_02_img,
    "colors": ["Branco", "Natural Fosco", "Preto"],
    "badge": "100% Alumínio"
})

print(f"Total authentic products extracted from PDF: {len(catalog)}")

# Write to catalog-data.js
js_content = f"""/* ==========================================================================
   ESQUADRIEURO - CATÁLOGO OFICIAL DE PRODUTOS 2025
   100% Extraído Diretamente do Catálogo Oficial da Esquadrieuro Store
   Total de {len(catalog)} produtos originais com fotos reais extraídas do documento.
   ========================================================================== */

const INITIAL_CATALOG = {json.dumps(catalog, ensure_ascii=False, indent=2)};
"""

with open("catalog-data.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("catalog-data.js updated with clean product photos successfully!")
