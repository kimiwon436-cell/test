import random, time, os, sys, threading

# 키 입력 처리 (스페이스바 입력 시 상승)
lift = False
def listen_input():
    global lift
    if os.name == 'nt':
        import msvcrt
        while True:
            if msvcrt.kbhit():
                msvcrt.getch(); lift = True
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                sys.stdin.read(1); lift = True
        finally: termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def run_balloon():
    global lift
    W, H = 50, 15
    balloon_y, v_y = H // 2, 0 # 시작 위치와 수직 속도
    obstacles = [] # [x, y, type]
    score = 0
    
    threading.Thread(target=listen_input, daemon=True).start()
    print("🎈 열기구 게임: 스페이스바를 눌러 열기를 채우세요(상승)!\n엔터를 누르면 시작합니다...")
    input()

    while True:
        # 1. 물리 엔진 (중력 vs 열기)
        if lift:
            v_y -= 0.8  # 위로 가속 (버너 점화)
            lift = False
        else:
            v_y += 0.3  # 중력으로 하락
        
        balloon_y += v_y
        
        # 2. 천장/바닥 충돌 체크
        if balloon_y < 0 or balloon_y >= H:
            print(f"\n💥 추락하거나 너무 높이 올라갔습니다! 점수: {score}")
            break

        # 3. 장애물 생성 (구름 '☁' 혹은 새 'v')
        if not obstacles or obstacles[-1][0] < W - 15:
            obstacles.append([W - 1, random.randint(1, H-2), random.choice(['☁', 'v'])])
        
        # 장애물 이동 및 필터링
        new_obstacles = []
        hit = False
        for x, y, char in obstacles:
            if x - 1 >= 0:
                if x - 1 == 5 and abs(y - int(balloon_y)) < 1: # 충돌 판정
                    hit = True
                new_obstacles.append([x - 1, y, char])
            else: score += 1
        obstacles = new_obstacles

        if hit:
            print(f"\n💥 장애물과 충돌했습니다! 점수: {score}")
            break

        # 4. 렌더링
        screen = [[" " for _ in range(W)] for _ in range(H)]
        
        # 장애물 그리기
        for x, y, char in obstacles:
            screen[y][x] = char
        
        # 열기구 그리기 (풍선과 바구니 모양)
        by = int(balloon_y)
        if 0 <= by < H: screen[by][5] = "O"   # 풍선
        if 0 <= by+1 < H: screen[by+1][5] = "U" # 바구니

        # 화면 출력
        out = f"ALTITUDE: {H-by}m | SCORE: {score}\n"
        out += "┌" + "-" * W + "┐\n"
        out += "\n".join(["|" + "".join(row) + "|" for row in screen]) + "\n"
        out += "└" + "-" * W + "┘"
        sys.stdout.write("\033[H" + out)
        sys.stdout.flush()
        
        time.sleep(0.08)

if __name__ == "__main__":
    run_balloon()
