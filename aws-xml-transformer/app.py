import streamlit as st
import boto3
import xml.etree.ElementTree as ET
from io import BytesIO
import json
from gpt4all import GPT4All

# -------------------- GPT4All Model --------------------
model_path = "C:/Users/Excalibur/.cache/gpt4all/"
model_name = "mistral-7b-instruct-v0.1.Q4_0.gguf"
gpt = GPT4All(model_name, model_path=model_path)

# -------------------- AWS S3 Settings --------------------
BUCKET_NAME = 'xml-chatbox-bucket'
s3 = boto3.client('s3')

# Find latest XML file in S3
def get_latest_xml_key(bucket_name):
    objects = s3.list_objects_v2(Bucket=bucket_name)
    if 'Contents' not in objects:
        return None
    xml_files = [obj for obj in objects['Contents'] if obj['Key'].endswith('.xml')]
    if not xml_files:
        return None
    latest_file = max(xml_files, key=lambda x: x['LastModified'])
    return latest_file['Key']

# Load XML file from S3
def load_xml_from_s3():
    key = get_latest_xml_key(BUCKET_NAME)
    if not key:
        st.error("S3 bucket'ta hiç XML dosyası bulunamadı.")
        st.stop()
    response = s3.get_object(Bucket=BUCKET_NAME, Key=key)
    xml_data = response['Body'].read()
    tree = ET.ElementTree(ET.fromstring(xml_data))
    return tree, tree.getroot(), key

# Save XML file back to S3
def save_xml_to_s3(tree, key):
    buffer = BytesIO()
    tree.write(buffer, encoding='utf-8', xml_declaration=True)
    s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=buffer.getvalue())

# -------------------- Uygulama --------------------
tree, root, current_key = load_xml_from_s3()
products = root.findall("product")

st.title("📦 Ürün Yönetim Paneli (S3 XML)")

# -------------------- Ürünleri Listele --------------------
st.subheader("📋 Mevcut Ürünler")
for i, product in enumerate(products):
    with st.expander(f"Ürün ID: {product.attrib.get('id', 'Bilinmiyor')}"):
        name = product.find("name").text if product.find("name") is not None else ""
        brand = product.find("brand").text if product.find("brand") is not None else ""
        price = product.find("price").text if product.find("price") is not None else ""
        features_elem = product.find("features")
        features = [f.text for f in features_elem.findall("feature")] if features_elem is not None else []
        stock = product.find("stock").text if product.find("stock") is not None else "?"

        st.write({"İsim": name, "Marka": brand, "Fiyat": price, "Stok": stock, "Özellikler": features})

        if st.button("🗑️ Sil", key=f"sil_{i}"):
            root.remove(product)
            save_xml_to_s3(tree, current_key)
            st.success("Ürün silindi.")
            st.experimental_rerun()

        with st.form(f"update_form_{i}"):
            st.markdown("### ✏️ Ürünü Güncelle")
            updated_name = st.text_input("İsim", value=name, key=f"name_{i}")
            updated_brand = st.text_input("Marka", value=brand, key=f"brand_{i}")
            updated_price = st.text_input("Fiyat", value=price, key=f"price_{i}")
            updated_features = st.text_area("Özellikler (virgülle)", value=", ".join(features), key=f"features_{i}")
            updated_stock = st.text_input("Stok", value=stock, key=f"stock_{i}")
            submit_update = st.form_submit_button("Güncelle")
            if submit_update:
                if product.find("name") is not None:
                    product.find("name").text = updated_name
                if product.find("brand") is not None:
                    product.find("brand").text = updated_brand
                if product.find("price") is not None:
                    product.find("price").text = updated_price
                features_elem = product.find("features")
                if features_elem is not None:
                    for f in list(features_elem):
                        features_elem.remove(f)
                else:
                    features_elem = ET.SubElement(product, "features")
                for feat in updated_features.split(","):
                    ET.SubElement(features_elem, "feature").text = feat.strip()
                stock_elem = product.find("stock")
                if stock_elem is None:
                    ET.SubElement(product, "stock").text = updated_stock
                else:
                    stock_elem.text = updated_stock
                save_xml_to_s3(tree, current_key)
                st.success("Ürün güncellendi.")
                st.experimental_rerun()

# -------------------- Yeni Ürün Ekleme --------------------
st.subheader("➕ Yeni Ürün Ekle")
with st.form("ekle_form"):
    new_id = st.text_input("Ürün ID")
    new_name = st.text_input("İsim")
    new_brand = st.text_input("Marka")
    new_price = st.text_input("Fiyat")
    new_stock = st.text_input("Stok")
    new_features = st.text_area("Özellikler (virgülle ayır)")
    ekle = st.form_submit_button("Ürünü Ekle")
    if ekle:
        new_product = ET.SubElement(root, "product", {"id": new_id})
        ET.SubElement(new_product, "name").text = new_name
        ET.SubElement(new_product, "brand").text = new_brand
        ET.SubElement(new_product, "price").text = new_price
        ET.SubElement(new_product, "stock").text = new_stock
        features_elem = ET.SubElement(new_product, "features")
        for feat in new_features.split(","):
            ET.SubElement(features_elem, "feature").text = feat.strip()
        save_xml_to_s3(tree, current_key)
        st.success("Ürün eklendi.")
        st.experimental_rerun()

# -------------------- GPT ile XML Güncelle --------------------
st.markdown("---")
st.subheader("🤖 GPT ile Doğal Dil Komutla XML Güncelle")

user_prompt = st.text_area("Doğal dil komutunuzu yazın:", key="gpt_input_json")
if st.button("Gönder ve Güncelle JSON"):
    with gpt.chat_session():
        prompt_text = f"""
Lütfen *yalnızca* geçerli JSON formatında ve başka hiçbir metin, açıklama veya boşluk eklemeden, aşağıdaki yapıya uygun olarak yanıt ver:

{user_prompt}

JSON formatı:
{{
  "action": "add" veya "update" veya "delete",
  "product": {{
    "name": "string",
    "price": int veya float,
    "stock": int,
    "brand": "string",
    "features": ["string", ...]
  }}
}}
"""
        gpt_response = gpt.generate(prompt_text)
        st.success("GPT yanıtı alındı:")
        st.code(gpt_response)

    try:
        cleaned = gpt_response[gpt_response.find('{'):]
        result = json.loads(cleaned)

        if result['action'] == 'add':
            new_product = ET.SubElement(root, 'product', {'id': str(len(products) + 1)})
            ET.SubElement(new_product, 'name').text = result['product']['name']
            ET.SubElement(new_product, 'price').text = str(result['product']['price'])
            ET.SubElement(new_product, 'stock').text = str(result['product']['stock'])
            ET.SubElement(new_product, 'brand').text = result['product'].get('brand', 'GPT')
            features_elem = ET.SubElement(new_product, 'features')
            for feat in result['product'].get('features', []):
                ET.SubElement(features_elem, "feature").text = feat
            save_xml_to_s3(tree, current_key)
            st.success("Yeni ürün eklendi.")

        elif result['action'] == 'update':
            updated = False
            for prod in root.findall('product'):
                if prod.find('name').text.lower() == result['product']['name'].lower():
                    prod.find('price').text = str(result['product']['price'])
                    prod.find('stock').text = str(result['product']['stock'])
                    brand_val = result['product'].get('brand', None)
                    if brand_val:
                        prod.find('brand').text = brand_val
                    features = result['product'].get('features', [])
                    features_elem = prod.find('features')
                    if features_elem is not None:
                        for f in list(features_elem):
                            features_elem.remove(f)
                    else:
                        features_elem = ET.SubElement(prod, 'features')
                    for feat in features:
                        ET.SubElement(features_elem, 'feature').text = feat
                    updated = True
                    break
            if updated:
                save_xml_to_s3(tree, current_key)
                st.success("Ürün güncellendi.")
            else:
                st.warning("Ürün bulunamadı.")

        elif result['action'] == 'delete':
            deleted = False
            for prod in root.findall('product'):
                if prod.find('name').text.lower() == result['product']['name'].lower():
                    root.remove(prod)
                    deleted = True
                    break
            if deleted:
                save_xml_to_s3(tree, current_key)
                st.success("Ürün silindi.")
            else:
                st.warning("Silinecek ürün bulunamadı.")

    except Exception as e:
        st.error(f"Hata oluştu: {e}")
