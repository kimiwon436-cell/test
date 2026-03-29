import pygame
import sys
import math

# --- 설정 및 상수 ---
SIZE = 15  # 15x15 오목판
CELL_SIZE = 40
MARGIN = 40
SCREEN_SIZE = CELL_SIZE * (SIZE - 1) + MARGIN * 2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARD_COLOR = (220, 179, 92)

# 난이도 설정 (탐색 깊이)
# 1: 하(Easy), 2: 중(Normal), 3: 상(Hard - 약간의 대기시간 발생)
DIFFICULTY_DEPTH = 2 

class OmokGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("AI 오목 - 난이도: " + str(DIFFICULTY_DEPTH))
        self.board = [[0] * SIZE for _ in range(SIZE)]
        self.turn = 1 # 1: 플레이어(흑), 2: AI(백)
        self.game_over = False

    def draw_board(self):
        self.screen.fill(BOARD_COLOR)
        for i in range(SIZE):
            # 가로선
            pygame.draw.line(self.screen, BLACK, [MARGIN, MARGIN + i * CELL_SIZE], [SCREEN_SIZE - MARGIN, MARGIN + i * CELL_SIZE], 1)
            # 세로선
            pygame.draw.line(self.screen, BLACK, [MARGIN + i * CELL_SIZE, MARGIN], [MARGIN + i * CELL_SIZE, SCREEN_SIZE - MARGIN], 1)
        
        for r in range(SIZE):
            for c in range(SIZE):
                if self.board[r][c] == 1:
                    pygame.draw.circle(self.screen, BLACK, [MARGIN + c * CELL_SIZE, MARGIN + r * CELL_SIZE], 18)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(self.screen, WHITE, [MARGIN + c * CELL_SIZE, MARGIN + r * CELL_SIZE], 18)

    def check_win(self, r, c, piece):
        directions = [(0,1), (1,0), (1,1), (1,-1)]
        for dr, dc in directions:
            count = 1
            # 양방향 탐색
            for i in range(1, 5):
                nr, nc = r + dr*i, c + dc*i
                if 0 <= nr < SIZE and 0 <= nc < SIZE and self.board[nr][nc] == piece: count += 1
                else: break
            for i in range(1, 5):
                nr, nc = r - dr*i, c - dc*i
                if 0 <= nr < SIZE and 0 <= nc < SIZE and self.board[nr][nc] == piece: count += 1
                else: break
            if count >= 5: return True
        return False

    # --- AI 로직 ---
    def evaluate_board(self):
        # 간단한 점수 평가 함수 (연속된 돌의 개수 기반)
        score = 0
        for r in range(SIZE):
            for c in range(SIZE):
                if self.board[r][c] != 0:
                    score += self.get_pos_score(r, c, self.board[r][c])
        return score

    def get_pos_score(self, r, c, piece):
        # 위치별 가산점 (중앙일수록 유리)
        return (7 - abs(7-r)) + (7 - abs(7-c))

    def minimax(self, depth, alpha, beta, maximizing):
        if depth == 0:
            return self.evaluate_board()

        moves = self.get_ordered_moves()
        if maximizing:
            max_eval = -math.inf
            for r, c in moves:
                self.board[r][c] = 2
                eval = self.minimax(depth - 1, alpha, beta, False)
                self.board[r][c] = 0
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha: break
            return max_eval
        else:
            min_eval = math.inf
            for r, c in moves:
                self.board[r][c] = 1
                eval = self.minimax(depth - 1, alpha, beta, True)
                self.board[r][c] = 0
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha: break
            return min_eval

    def get_ordered_moves(self):
        # 최적화를 위해 돌이 놓인 주변만 탐색
        moves = []
        for r in range(SIZE):
            for c in range(SIZE):
                if self.board[r][c] == 0:
                    # 주변에 돌이 있는지 확인 (성능 최적화)
                    has_neighbor = False
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            nr, nc = r+dr, c+dc
                            if 0 <= nr < SIZE and 0 <= nc < SIZE and self.board[nr][nc] != 0:
                                has_neighbor = True; break
                        if has_neighbor: break
                    if has_neighbor or (r == 7 and c == 7): # 첫 수는 중앙
                        moves.append((r, c))
        return moves

    def ai_move(self):
        best_score = -math.inf
        best_move = None
        for r, c in self.get_ordered_moves():
            self.board[r][c] = 2
            if self.check_win(r, c, 2): # 바로 이길 수 있으면 둔다
                return (r, c)
            score = self.minimax(DIFFICULTY_DEPTH, -math.inf, math.inf, False)
            self.board[r][c] = 0
            if score > best_score:
                best_score = score
                best_move = (r, c)
        return best_move

    def run(self):
        while not self.game_over:
            self.draw_board()
            pygame.display.update()

            if self.turn == 2: # AI 차례
                r, c = self.ai_move()
                self.board[r][c] = 2
                if self.check_win(r, c, 2):
                    print("AI 승리!")
                    self.game_over = True
                self.turn = 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.turn == 1:
                    x, y = event.pos
                    c = round((x - MARGIN) / CELL_SIZE)
                    r = round((y - MARGIN) / CELL_SIZE)
                    
                    if 0 <= r < SIZE and 0 <= c < SIZE and self.board[r][c] == 0:
                        self.board[r][c] = 1
                        if self.check_win(r, c, 1):
                            print("플레이어 승리!")
                            self.game_over = True
                        self.turn = 2

        # 결과 출력 후 대기
        self.draw_board()
        pygame.display.update()
        pygame.time.wait(3000)

if __name__ == "__main__":
    game = OmokGame()
    game.run()
