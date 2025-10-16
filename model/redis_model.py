import redis


class Redis_model:
    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379, db=0)
        
    def verificacao_redis(self) -> bool:
        try:
            self.client.ping()
            return True
        except redis.ConnectionError:
            return False
        
    def salvar_mensagem(self, id_usuario: int, role: str, mensagem: str) ->bool:
        try:
            self.client.rpush(f"conversa:{id_usuario}", f"{role}:{mensagem}")
            return True
        except Exception as e:
            print(f"Erro ao salvar mensagem no Redis: {e}")
            return False
        
    def buscar_conversa(self, id_usuario: int):
        try:
            mensagens = self.client.lrange(f"conversa:{id_usuario}", 0, -1)
            conversa = []
            for msg in mensagens:
                role, content = msg.decode('utf-8').split(':', 1)
                conversa.append({"role": role, "content": content})
            return conversa
        except Exception as e:
            print(f"Erro ao buscar conversa no Redis: {e}")
            return []
    
    def limpar_conversa(self, id_usuario: int) -> bool:
        try:
            self.client.delete(f"conversa:{id_usuario}")
            return True
        except Exception as e:
            print(f"Erro ao limpar conversa no Redis: {e}")
            return False