from bot import AI_TOKEN
from openai import OpenAI


class Bot_AI:
    def __init__(self, token: str=AI_TOKEN) -> None:
        self._client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=token,
        )

    def answer(self, message: str) -> str:
        completion = self._client.chat.completions.create(
            model="deepseek/deepseek-chat-v3.1",
            messages=[
                {
                    "role": 'user',
                    "content": (f'Представь что ты ИИ помощник для людей попавший в виртуальные симуляции экстренных '
                                f'ситуаций. Ты должен отвечать на вопросы так чтобы твой текст ответа мог быть без '
                                f'изменений отправлен в социальную сеть телеграмм без хэштегов. Твой ответ должен быть '
                                f'из пунктов действий при данной экстренной ситуации. Ответ должен содержать только '
                                f'пункты действий при экстренной ситуации. '
                                f'Пользователь дал тебе экстренную ситуация {message}')
                }
            ]
        )
        return completion.choices[0].message.content


test = Bot_AI()
print(test.answer('Теракт'))




