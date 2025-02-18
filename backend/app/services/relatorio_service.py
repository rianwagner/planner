from ..models.materia_model import Materia
from ..models.prova_model import Prova
from ..models.trabalho_model import Trabalho
from sqlalchemy import and_
from datetime import datetime

class RelatorioService:
    @staticmethod
    def gerar_relatorio_por_materia(user_id, data_inicio=None, data_fim=None):
        try:
            materias = Materia.query.filter_by(user_id=user_id).all()
            relatorio = []
            for materia in materias:
                filtro_provas = [Prova.materia_id == materia.id, Prova.user_id == user_id]
                if data_inicio:
                    filtro_provas.append(Prova.data_prova >= data_inicio)
                if data_fim:
                    filtro_provas.append(Prova.data_prova <= data_fim)

                filtro_trabalhos = [Trabalho.materia_id == materia.id, Trabalho.user_id == user_id]
                if data_inicio:
                    filtro_trabalhos.append(Trabalho.data_entrega >= data_inicio)
                if data_fim:
                    filtro_trabalhos.append(Trabalho.data_entrega <= data_fim)

                provas = Prova.query.filter(and_(*filtro_provas)).order_by(Prova.data_prova).all()
                trabalhos = Trabalho.query.filter(and_(*filtro_trabalhos)).order_by(Trabalho.data_entrega).all()
                
                materia_info = {
                    "materia_id": materia.id,
                    "materia_nome": materia.nome,
                    "provas": [{
                        "id": prova.id,
                        "titulo": prova.titulo,
                        "descricao": prova.descricao,
                        "data": prova.data_prova.strftime("%Y-%m-%d")
                    } for prova in provas],
                    "trabalhos": [{
                        "id": trabalho.id,
                        "titulo": trabalho.titulo,
                        "descricao": trabalho.descricao,
                        "data": trabalho.data_entrega.strftime("%Y-%m-%d")
                    } for trabalho in trabalhos]
                }
                
                relatorio.append(materia_info)
            
            return relatorio
        except Exception as e:
            print(f"Erro ao gerar relatório: {e}")
            raise e