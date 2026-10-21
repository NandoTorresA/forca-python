import os
from texts import game_over_text, victory_text




def mask(answer: str) -> str:
    '''
    Essa função mascara a palavra resposta. Transformando os dígitos em asteriscos, com exceção do espaço e do hífen
    '''
    masked_word = ''
    for char in answer:
        masked_word += '*' if char not in " -" else char
    return masked_word


def check_try(used_chars: list[str]) -> str:
    '''
    Essa função verifica se o input do player é válido. Verifica se o campo está vazio, se o campo tem apenas uma letra, se a letra já foi
    escolhida e se não tem número. Com a única exceção do número 1, que aciona a função all_win()
    '''

    while True:
        char = (input('Digite uma letra: ')).lower().strip()
        if not char:
            print('Campo vazio, digite algo')
        elif len(char) > 1:
            print('Digite apenas uma letra')
        elif char in used_chars:
            print('Letra já escolhida')
        elif char == '1':
            return '1'
        elif not char.isalpha():
            print('Digite apenas letras')
        else:
            return char



def check_answer() -> str:
    '''
    Essa função verifica os critérios da palavra resposta.
    Verifica se o campo está vazio, se tem mais de 50 caracteres, se tem menos de 4 caracteres ou contém números
    '''
    while True:
        answer_word = (input('Digite a palavra resposta: ')).lower().strip()
        if not answer_word:
            print('Resposta vazia, digite algo')
        elif len(answer_word) > 50:
            print('Palavra muito longa')
        elif len(answer_word) < 4:
            print('Palavra muito curta, digite uma palavra com pelo menos 4 letras')
        elif not all(char.isalpha() or char in '- ' for char in answer_word):
            print('Use apenas letras espaços e hífens')
        else:
            return answer_word


def clear_screen():
    '''Essa função limpa o terminal'''
    os.system('cls' if os.name == 'nt' else 'clear')


def check_guess() -> str | None:
    '''
    Essa função verifica a validade do input da função all_win()
    Verificando se ela está vazia ou contém números
    '''
    while True:
        word = (input('Digite a palavra que deseja arriscar: ')).lower().strip()
        if not word:
            return
        elif not all(char.isalpha() or char in '- ' for char in word):
            print('Use apenas letras espaços e hífens')
        else:
            return word


def all_win():
    '''
    Essa função aciona a função para arriscar a palavra com um palpite.
    Mostra o aviso de risco no terminal e a instrução para voltar ao jogo normal
    Retorna a o retorno da função check_guess()
    '''
    clear_screen()
    print('Advertência: errar a palavra ocasiona a perda imediata do jogo!\nPara voltar, envie o campo vazio')
    return check_guess()


def display(current_answer: str, tries: int, used_chars: list[str], forca_draw: list[str], max_tries: int):
    '''
    Limpa o terminal e exibe as informações na tela.
    Exibe A instrução de digitar uma letra, a palavra atual, número de tentativas, letras utilizadas e a 
    instrução para acionar o all_win()
    '''
    clear_screen()
    print(f'''Digite apenas uma letra
palavra atual: {current_answer}
Tentativas falhas: {tries}/{max_tries}
{forca_draw[tries]}
Letras utilizadas: {', '.join(used_chars)}
Aperte 1 para arriscar a palavra completa''')


def lose_display(answer: str):
    '''Limpa o terminal e exibe a tela de derrota e a palavra'''
    clear_screen()
    print(game_over_text)
    print(f'Você perdeu!\nA palavra era: {answer}')


def win_display(answer: str):
    '''Limpa o terminal e exibe a tela de vitória e a resposta'''
    clear_screen()
    print(victory_text)
    print(f'Você venceu!\nA palavra era {answer}')


draws = [
    r"""
       +---+
       |   |
       |   
       |   
       |   
       |   
    =========
    """,
    r"""
       +---+
       |   |
       |   O
       |   
       |   
       |   
    =========
    """,
    r"""
       +---+
       |   |
       |   O
       |   |
       |   
       |   
    =========
    """,
    r"""
       +---+
       |   |
       |   O
       |  /|
       |   
       |   
    =========
    """,
    r"""
       +---+
       |   |
       |   O
       |  /|\
       |   
       |   
    =========
    """,
    r"""
       +---+
       |   |
       |   O
       |  /|\
       |    \
       |   
    =========
    """,
    r"""
       +---+
       |   |
       |   O
       |  /|\
       |  / \
       |   
    =========
    """
]


def main():
    answer = check_answer()
    tries = 0
    used_chars = []
    max_tries = len(draws) - 1
    current_word = mask(answer=answer)

    while True:
        display(current_answer=current_word, tries=tries, used_chars=used_chars, forca_draw=draws, max_tries=max_tries)
        player_try = check_try(used_chars=used_chars)

        if player_try == '1':
            player_guess = all_win()
            if player_guess:
                if answer != player_guess:
                    tries = max_tries
                else:
                    current_word = answer

        else:
            positions = [i for i, char in enumerate(answer) if player_try == char]
            if positions:
                current_word_list = list(current_word)
                for i in positions:
                    current_word_list[i] = player_try
                current_word = ''.join(current_word_list)
            else:
                tries += 1
            used_chars.append(player_try)

        if tries >= max_tries:
            lose_display(answer=answer)
            print(draws[max_tries])
            break
        elif current_word == answer:
            win_display(answer=answer)
            break

if __name__ == '__main__':
    main()