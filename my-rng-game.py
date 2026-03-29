import random
import time

def start_game():
    lv, gold = 0, 500  # 초기 레벨과 골드
    weps = ["목검", "철검", "은검", "황금검", "광선검", "전설의 검"]
    w_idx = 0
    
    print("=== 🛠️ 무기 강화 시뮬레이터 ===")
    print("성공하면 레벨 업! 실패하면 하락이나 파괴! 판매(n)로 돈을 버세요.")

    while True:
        cur_w = weps[w_idx]
        # 강화 비용과 판매 가격 계산
        cost = 100 + (lv * 60)
        sell_price = (lv * 150) + (lv**2 * 50) + 100
        # 성공 확률 계산
        if lv < 5: suc = 90 - (lv * 10)
        elif lv < 10: suc = 40 - (lv - 5) * 5
        else: suc = max(1, 15 - (lv - 10) * 2)

        print(f"\n[+{lv} {cur_w}] | 보유 골드: {gold}G")
        print(f"1. 강화(y): {cost}G (확률: {suc}%)")
        print(f"2. 판매(n): +{sell_price}G 획득 (0강 초기화)")
        print(f"3. 무기변경(c) | 종료(q)")
        
        choice = input("선택: ").lower()

        if choice == 'q':
            print("게임을 종료합니다.")
            break
        
        elif choice == 'n':
            gold += sell_price
            print(f"💰 {cur_w}를 판매하여 {sell_price}G를 벌었습니다!")
            lv = 0 # 판매 후 초기화
            
        elif choice == 'c':
            w_idx = (w_idx + 1) % len(weps)
            print(f"🔄 무기를 [{weps[w_idx]}] (으)로 바꿨습니다!")

        elif choice == 'y':
            if gold < cost:
                print("❌ 골드가 부족합니다! 무기를 판매해서 돈을 버세요.")
                continue
            
            gold -= cost
            print("강화 시도 중.", end="")
            for _ in range(2): time.sleep(0.4); print(".", end="", flush=True)
            
            if random.randint(1, 100) <= suc:
                lv += 1
                print(f"\n✨ 성공! [+{lv} {cur_w}]가 되었습니다!")
                if lv == 15: print("🎊 축하합니다! 최종 단계 달성! 🎊")
            else:
                print("\n❌ 실패!", end=" ")
                if lv >= 10 and random.random() < 0.15:
                    print("💥 아이템이 파괴되었습니다! (0강 초기화)")
                    lv = 0
                elif lv >= 5:
                    lv -= 1
                    print("단계가 하락했습니다. (-1)")
                else:
                    print("다행히 단계가 유지되었습니다.")
        else:
            print("잘못된 입력입니다.")

if __name__ == "__main__":
    start_game()
