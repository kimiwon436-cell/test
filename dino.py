import random, time, os, sys, threading

# 키 입력 감지 (윈도우/맥/리눅스 공통)
key_pressed = False
def listen_input():
    global key_pressed
    if os.name == 'nt':
        import msvcrt
        while True:
            if msvcrt.kbhit():
                msvcrt.getch()
                key_pressed = True
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            while True:
                sys.stdin.read(1)
                key_pressed = True
        finally: termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def run_game():
    global key_pressed
    W, H = 60, 15
    dino_y, v_y = 0, 0
    ground_y = H - 3
    obstacles = []
    score = 0
    
    # 공룡 모양 (2줄 자산)
    dino_art = [" Gp ", " d b"] # 🦖 대신 문자 조합
    cactus_art = "|" # 🌵 대신 문자 조합

    threading.Thread(target=listen_input, daemon=True).start()
    
    print("스페이스바를 눌러 점프! 시작하려면 엔터...")
    input()

    while True:
        # 1. 물리 엔진 (점프)
        if key_pressed and dino_y == 0:
            v_y = 2.5 # 점프 힘
            key_pressed = False
        
        dino_y += v_y
        if dino_y > 0: v_y -= 0.5 # 중력
        else: dino_y, v_y = 0, 0

        # 2. 장애물 생성 및 이동
        if not obstacles or obstacles[-1] < W - random.randint(15, 30):
            obstacles.append(W - 1)
        
        obstacles = [o - 1 for o in obstacles if o > 0]

        # 3. 충돌 체크
        for o in obstacles:
            if o == 5 and dino_y < 1: # 공룡 위치(5)에서 땅에 있으면 충돌
                print(f"\n💥 충돌! 최종 점수: {score}")
                return

        # 4. 화면 렌더링 (리스트 버퍼 사용)
        screen = [[" " for _ in range(W)] for _ in range(H)]
        
        # 바닥 그리기
        for x in range(W): screen[ground_y+1][x] = "="
        
        # 공룡 그리기 (y좌표 반전 처리)
        dy = ground_y - int(dino_y)
        for i, line in enumerate(dino_art):
            if 0 <= dy-1+i < H:
                for j, char in enumerate(line):
                    if char != " ": screen[dy-1+i][5+j] = char

        # 장애물 그리기
        for o in obstacles:
            if 0 <= o < W: screen[ground_y][o] = cactus_art

        # 출력 (화면 깜빡임 방지)
        out = f"SCORE: {score}\n"
        out += "\n".join(["".join(row) for row in screen])
        sys.stdout.write("\033[H" + out)
        sys.stdout.flush()
        
        score += 1
        time.sleep(0.05)

if __name__ == "__main__":
    run_game()
