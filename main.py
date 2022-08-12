import requests
import json
import pandas as pd

def buscar_dados_shipment(shippingID):
  request_shipment = requests.get(f'https://6f008c57-99e0-4a2e-8d80-782a71cf99db.mock.pstmn.io/shipments/{shippingID}?caller.id=661750045')
  shipment = json.loads(request_shipment.content)
  
  entityShipment = {
    'shipmentID': shipment['id'],
    'tipoLogistica': shipment['logistic_type'],
    'estado': shipment['status'],
    'subestado': shipment['substatus'],
    'depositoOuVendedor': 'Depósito' if shipment['logistic_type'] == 'fulfillment' else 'Vendedor',
    'destinoEnvio': shipment['sender_address']['agency'],
    'enderecoReceptor': shipment['receiver_address']['address_line'] + ' ' + shipment['receiver_address']['city']['name']  + ' ' + shipment['receiver_address']['zip_code'],
    'enderecoEnvio': shipment['sender_address']['address_line'] + ' ' + shipment['sender_address']['city']['name']  + ' ' + shipment['sender_address']['zip_code'],
  }

  return entityShipment

def buscar_dados_orderId(orderID):
  request_order = requests.get(f'https://6f008c57-99e0-4a2e-8d80-782a71cf99db.mock.pstmn.io/orders/{orderID}?caller.id=661750045')
  order = json.loads(request_order.content)

  entityOrder = {
  'orderID': order['id'],
  # 'itemID': [x['item']['id'] for x in order['order_items']],
  'itemID': order['order_items'][0]['item']['id'],
  'descricaoProduto': 
    order['order_items'][0]['item']['title'] + ' ' + 
    order['order_items'][0]['item']['variation_attributes'][0]['name'] + ' '+
    order['order_items'][0]['item']['variation_attributes'][0]['value_name'],
  'custoTotalOrdem': order['total_amount'],
  'moedaUtilizada': order['currency_id'],
  }

  return {
   'entityOrder': entityOrder,
   'entityShipment': buscar_dados_shipment(order['shipping']['id'])
  }

def exportarCSV():
    orderIDs = ['4114988927', '4114988960', '4114999549']
    data = []
    for x in orderIDs:
      data.append(buscar_dados_orderId(x))

    datas = {
      'ID do Pedido': [x['entityOrder']['orderID'] for x in data],
      'ID do Item': [x['entityOrder']['itemID'] for x in data],
      'Descrição do produto': [x['entityOrder']['descricaoProduto'] for x in data],
      'Custo total da ordem': [x['entityOrder']['custoTotalOrdem'] for x in data],
      'Moeda utilizada': [x['entityOrder']['moedaUtilizada'] for x in data],
      'ID do Envio': [x['entityShipment']['shipmentID'] for x in data],
      'Tipo de logística': [x['entityShipment']['tipoLogistica'] for x in data],
      'Estado': [x['entityShipment']['estado'] for x in data],
      'Subestado': [x['entityShipment']['subestado'] for x in data],
      'Depósito ou vendedor?': [x['entityShipment']['depositoOuVendedor'] for x in data],
      'Destino': [x['entityShipment']['destinoEnvio'] for x in data],
      'Endereço do Receptor': [x['entityShipment']['enderecoReceptor'] for x in data],
      'Endereço de Envio': [x['entityShipment']['enderecoEnvio'] for x in data],
    }
    # df = json_normalize(buscar_dados_orderId('4114988927')['entityOrder'])
    df = pd.DataFrame(datas)
    df.to_csv("data.csv", index = False)
    print(df)

if __name__ == '__main__':
  exportarCSV()


