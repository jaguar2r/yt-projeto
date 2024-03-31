from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip
import math

def criar_loop_musica(caminho_original, caminho_saida, duracao_desejada_em_minutos):
    """
    Esta função cria um loop contínuo de um arquivo de música em formato MP3, exportando o resultado final.

    Args:
        caminho_original (str): O caminho do arquivo de música original em formato MP3.
        caminho_saida (str): O caminho onde o arquivo de música loopado será salvo.
        duracao_desejada_em_minutos (float): A duração desejada para o loop da música em minutos.

    A função carrega o arquivo MP3 especificado, calcula o número de repetições necessárias
    para atingir a duração desejada e cria um loop da música. A música loopada é então cortada para
    garantir que a duração final corresponda exatamente à duração desejada. O arquivo resultante é
    exportado para o caminho de saída especificado, também em formato MP3.
    """
    musica = AudioSegment.from_mp3(caminho_original)

    repeticoes_necessarias = math.ceil((duracao_desejada_em_minutos * 60000) / len(musica))

    musica_loop = musica * repeticoes_necessarias

    musica_loop = musica_loop[:int(duracao_desejada_em_minutos * 60000)]

    musica_loop.export(caminho_saida, format="mp3")

    print(f'Música loopada exportada com sucesso: {caminho_saida}')

def criar_n_loop_musica(caminho_original, caminho_saida, repeticoes):
    """
    Cria um loop de um arquivo de música especificado por um número definido de vezes.

    Args:
        caminho_original (str): Caminho para o arquivo de áudio original.
        caminho_saida (str): Caminho para o arquivo de saída onde a música loopada será salva.
        repeticoes (int): Número de vezes que a música será repetida.

    Esta função carrega um arquivo de música no formato MP3, determina sua duração em segundos,
    realiza o loop da música pelo número de vezes especificado no parâmetro `repeticoes` e
    exporta o resultado para um novo arquivo MP3. A duração original e a duração após edição são
    impressas, assim como uma confirmação de sucesso ao final da exportação.
    """
    musica = AudioSegment.from_mp3(caminho_original)

    duracao_original_segundos = len(musica) / 1000
    print(f"Duração original da música: {duracao_original_segundos} segundos")

    musica_loop = musica * repeticoes

    duracao_editada_segundos = len(musica_loop) / 1000
    print(f"Duração da música após edição: {duracao_editada_segundos} segundos")

    musica_loop.export(caminho_saida, format="mp3")

    print(f'Música loopada exportada com sucesso: {caminho_saida}')

def ajustar_video_para_audio(video_path, audio_path, video_saida):
    """
    Sincroniza um arquivo de vídeo com um arquivo de áudio ajustando suas durações e exporta o resultado.

    Args:
        video_path (str): O caminho para o arquivo de vídeo original.
        audio_path (str): O caminho para o arquivo de áudio que será sincronizado com o vídeo.
        video_saida (str): O caminho para o arquivo de vídeo resultante.

    A função carrega os clipes de vídeo e áudio, compara suas durações e realiza ajustes:
    - Se o áudio for mais curto que o vídeo, o vídeo será cortado para a duração do áudio.
    - Se o áudio for mais longo que o vídeo, o vídeo será repetido em loop até corresponder à duração do áudio.

    O clipe de vídeo resultante terá o áudio substituído pelo áudio carregado e será exportado para o caminho especificado,
    usando o codec 'libx264' para vídeo e 'aac' para áudio.

    Após a conclusão, uma mensagem de sucesso será impressa com o caminho do vídeo exportado.
    """
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    video_duration = video_clip.duration
    audio_duration = audio_clip.duration

    if audio_duration < video_duration:
        video_clip = video_clip.subclip(0, audio_duration)
    else:
        video_clip = video_clip.loop(duration=audio_duration)

    video_clip = video_clip.set_audio(audio_clip)

    video_clip.write_videofile(video_saida, codec='libx264', audio_codec='aac')

    print(f'Vídeo ajustado exportado com sucesso: {video_saida}')

def juntar_varias_musicas(caminhos_musicas, nome_musicas, caminho_saida):
    """
    Concatena várias músicas em uma única faixa de áudio e exporta o resultado.

    Args:
        caminhos_musicas (str): O caminho base onde as músicas estão localizadas. Este caminho será
                                prefixado a cada nome de música fornecido na lista `nome_musicas`.
        nome_musicas (list): Uma lista contendo os nomes dos arquivos de música (incluindo extensões)
                             a serem concatenados. Assume-se que todas as músicas estão no mesmo formato.
        caminho_saida (str): O caminho completo, incluindo o nome do arquivo e extensão, para onde a
                             música concatenada será exportada.

    A função inicia criando uma lista de caminhos completos para as músicas, usando a concatenação do
    `caminhos_musicas` com cada item em `nome_musicas`. Em seguida, carrega a primeira música da lista
    para iniciar a faixa final. As músicas subsequentes são então carregadas uma a uma e concatenadas
    à faixa final. A música resultante é exportada para o `caminho_saida` especificado, em formato MP3.

    Nota:
        - Assegure-se de que todas as músicas estejam no mesmo formato e taxa de amostragem para evitar
          problemas de compatibilidade durante a concatenação.
        - A instalação do ffmpeg ou libav é necessária, pois o pydub depende deles para processar
          arquivos MP3.
    """
    lista_caminhos_musicas = [caminhos_musicas + item for item in nome_musicas]

    musica_final = AudioSegment.from_file(lista_caminhos_musicas[0])

    for caminho_musica in lista_caminhos_musicas[1:]:
        musica_atual = AudioSegment.from_file(caminho_musica)
        musica_final += musica_atual

    musica_final.export(caminho_saida, format="mp3")
