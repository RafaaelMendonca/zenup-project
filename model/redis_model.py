import redis
import json
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class RedisModel:
    def __init__(self, host='localhost', port=6379, db=0, decode_responses=True):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=decode_responses)
        
    def verificacao_redis(self) -> bool:
        try:
            return self.client.ping()
        except redis.ConnectionError as e:
            logger.error(f"Redis connection error: {e}")
            return False
        
    def salvar_mensagem(self, id_usuario: int, role: str, mensagem: str) -> bool:
        try:
            data = json.dumps({"role": role, "content": mensagem})
            self.client.rpush(f"conversa:{id_usuario}", data)
            return True
        except redis.RedisError as e:
            logger.error(f"Erro ao salvar mensagem no Redis: {e}")
            return False
        
    def buscar_conversa(self, id_usuario: int) -> List[Dict[str, str]]:
        try:
            mensagens = self.client.lrange(f"conversa:{id_usuario}", 0, -1)
            conversa = [json.loads(msg) for msg in mensagens]
            return conversa
        except (redis.RedisError, json.JSONDecodeError) as e:
            logger.error(f"Erro ao buscar conversa no Redis: {e}")
            return []
    
    def limpar_conversa(self, id_usuario: int) -> bool:
        try:
            self.client.delete(f"conversa:{id_usuario}")
            return True
        except redis.RedisError as e:
            logger.error(f"Erro ao limpar conversa no Redis: {e}")
            return False
