import random
import time
import os
import sys
import threading

# 터미널 화면을 지우는 함수 (윈도우/맥/리눅스 호환)
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# 키입력을 비동기로 받기 위한 변수
key_input = None

def get_input():
    global key_input
    # 운영체제별 키 입력 방식 처리 (윈도우: msvcrt, 맥/리눅스: sys.stdin)
    if os.name == 'nt':
        import msvcrt
        while True:
            if msvcrt.kbhit():
                key_input = msvcrt.getch().decode().lower()
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            while True:
                key_input = sys.stdin.read(1).lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def game():
    global key_input
    WIDTH = 50       # 게임 화면 너비
    HEIGHT = 12      # 게임 화면 높이
    DINO_Y = HEIGHT - 2 # 공룡의 기본 땅 높이
    
    # 공룡 애니메이션 프레임 (달리는 모습)
    dino_frames = ["🦖", "🐉"] 
    dino_jump = "🦅" # 점프할 때 모습
    dino_dead = "💥" # 부딪혔을 때 모습

    dino_pos = DINO_Y
    jump_timer = 0
    obstacles = []
    score = 0
    frame_count = 0
    game_over = False

    # 키 입력 스레드 시작
    input_thread = threading.Thread(target=get_input, daemon=True)
    input_thread.start()

    print("\n=== 🦖 터미널 공룡 달리기 ===\n")
    print("스페이스바(Space)나 'j' 키를 눌러 점프하세요!")
    print("준비되면 엔터(Enter)를 누르세요...")
    input()
    clear()

    while not game_over:
        frame_count += 1
        
        # 1. 점프 로직 처리
        if (key_input == ' ' or key_input == 'j') and dino_pos == DINO_Y:
            jump_timer = 5 # 점프 높이/시간
            key_input = None # 입력 초기화

        if jump_timer > 0:
            dino_pos = DINO_Y - 3 # 점프 중 위치
            jump_timer -= 1
        else:
            dino_pos = DINO_Y # 땅 위에 위치

        # 2. 장애물 생성 및 이동 로직 (레벨 디자인)
        if frame_count % random.randint(10, 20) == 0:
            obstacles.append(WIDTH - 2) # 새 장애물을 오른쪽 끝에 생성
        
        # 장애물 이동 (왼쪽으로) 및 충돌 체크
        for i in range(len(obstacles)):
            obstacles[i] -= 2 # 장애물 속도
            if obstacles[i] == 2 and dino_pos == DINO_Y:
                game_over = True # 충돌!
            if obstacles[i] < 0:
                score += 10 # 장애물 피하면 점수 획득
        
        # 화면 밖으로 나간 장애물 제거
        obstacles = [o for o in obstacles if o >= 0]

        # 3. 화면 그리기 (렌더링)
        scene = []
        for y in range(HEIGHT):
            row = [" "] * WIDTH
            if y == HEIGHT - 1: # 바닥 그리기
                row = ["="] * WIDTH
            
            # 장애물(선인장) 그리기
            for o in obstacles:
                if 0 <= o < WIDTH and y == DINO_Y:
                    row[o] = "🌵" 
            
            # 공룡 그리기
            if y == dino_pos:
                if game_over:
                    row[2] = dino_dead
                elif dino_pos < DINO_Y:
                    row[2] = dino_jump # 점프 중 모습
                else:
                    row[2] = dino_frames[frame_count % 2] # 달리는 모습 애니메이션
            
            scene.append("".join(row))

        # 버퍼에 한 번에 출력 (깜빡임 최소화)
        output = f"\nScore: {score:05}\n"
        output += "\n".join(scene)
        sys.stdout.write("\033[H" + output) # 커서를 맨 위로 올려서 덮어쓰기
        sys.stdout.flush()

        time.sleep(0.1) # 게임 속도 조절

    # 게임 오버 화면 출력
    clear()
    print(f"\n💥 GAME OVER 💥\n최종 점수: {score}\n")

if __name__ == "__main__":
    game()
