import tkinter as tk
import random

class DinoGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Dino Run (Space: Jump)")
        self.canvas = tk.Canvas(self.root, width=600, height=200, bg='white')
        self.canvas.pack()

        # 공룡(초록색)과 점수 설정
        self.dino = self.canvas.create_rectangle(50, 150, 80, 180, fill='green')
        self.score = 0
        self.score_text = self.canvas.create_text(550, 20, text="Score: 0")
        
        self.obstacles = []
        self.v_y = 0  # 세로 속도
        self.is_jumping = False
        self.game_over = False

        self.root.bind("<space>", self.jump)
        self.update()
        self.spawn_obstacle()
        self.root.mainloop()

    def jump(self, event):
        if not self.is_jumping and not self.game_over:
            self.v_y = -15 # 점프 힘
            self.is_jumping = True

    def spawn_obstacle(self):
        if not self.game_over:
            # 장애물 생성 (빨간색)
            h = random.randint(20, 50)
            o = self.canvas.create_rectangle(600, 180-h, 620, 180, fill='red')
            self.obstacles.append(o)
            # 다음 장애물 생성 간격 랜덤 (1~2초)
            self.root.after(random.randint(1000, 2000), self.spawn_obstacle)

    def update(self):
        if not self.game_over:
            # 중력 적용
            self.canvas.move(self.dino, 0, self.v_y)
            d_pos = self.canvas.coords(self.dino)
            
            if d_pos[3] < 180: # 공중에 떠있을 때
                self.v_y += 1 # 중력 가속도
            else: # 땅에 닿았을 때
                self.canvas.coords(self.dino, 50, 150, 80, 180)
                self.v_y = 0
                self.is_jumping = False

            # 장애물 이동 및 충돌 체크
            for o in self.obstacles[:]:
                self.canvas.move(o, -7, 0) # 장애물 속도
                o_pos = self.canvas.coords(o)
                
                if o_pos[2] < 0: # 화면 밖으로 나가면 삭제
                    self.canvas.delete(o)
                    self.obstacles.remove(o)
                    self.score += 1
                    self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

                # 충돌 감지 로직
                if d_pos[2] > o_pos[0] and d_pos[0] < o_pos[2] and d_pos[3] > o_pos[1]:
                    self.game_over = True
                    self.canvas.create_text(300, 100, text="GAME OVER", font=("Arial", 25), fill="black")

            self.root.after(20, self.update) # 20ms마다 화면 갱신

if __name__ == "__main__":
    DinoGame()
