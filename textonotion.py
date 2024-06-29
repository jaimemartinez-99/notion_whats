"""
Reads from text file and sends to Notion

"""
from notion.client import NotionClient
from notion_client import Client
from tokenprivado import token_notion, token_page, token_database


def write_text(client, page_id, text, type):
    client.blocks.children.append(
        block_id=page_id,
        children=[
            {
                "object": "block",
                "type": type,
                type: {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": text
                            }
                        }
                    ]
                }
            }
        ]
    )

def write_row(client, database_id):
    with open('mensajes.txt', 'r') as f:
        lines = f.readlines()  # Lee todas las líneas del archivo
        for line in lines:
            tipo, desc, timestamp = line.split(';', 2)
            client.pages.create(
                parent={"database_id": database_id},
                properties={
                    "Descripcion": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": desc
                                }
                            }
                        ]
                    },
                    "Tipo": {
                        "select": 
                            {
                                "name": tipo
                            }
                    },
                    "Timestamp": {
                        "title": [
                            {
                                "text": {
                                    "content": timestamp
                                }
                            }
                        ]
                    }
                }
            )

    # Copia los mensajes a un nuevo archivo de texto
    with open('mensajes_copiados.txt', 'w') as f:
        f.writelines(lines)

    # Borra las entradas del archivo 'mensajes.txt'
    open('mensajes.txt', 'w').close()
        
def main():
    client = Client(auth=token_notion)
    write_row(client, token_database)
    print('Done!')
if __name__ == '__main__':
    main()