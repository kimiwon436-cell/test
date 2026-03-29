import random, time

def game():
    lv, gold = 0, 1000
    weps = ["목검", "철검", "레이저 소드", "용살검", "운석 단검", "관리자 권한"]
    w_idx = 0
    
    print("=== 🛠️ 강화 & 판매 시뮬레이터 (사냥 없음) ===")
    print("[y] 강화 | [n] 판매(돈벌기) | [c] 무기교체 | [q] 종료")

    while True:
        # 현재 무기와 가격/확률 설정
        cur_w = weps[w_idx]
        cost = 100 + (lv * 70)
        sell_val = (lv * 200) + (lv**2 * 100) # 레벨이 높을수록 비쌈
        suc = max(5, 90 - (lv * 8)) # 최소 확률 5%

        print(f"\n----------------------------------------")
        print(f"상태: [+{lv} {cur_w}] | 보유 골드: {gold}G")
        print(f"가격: 강화 {cost}G (확률 {suc}%) | 판매 시 {sell_val}G 획득")
        
        cmd = input("명령(y, n, c, q): ").lower()

        if cmd == 'y': # 강화 로직
            if gold < cost:
                print("❌ 돈이 없어요! 지금 무기를 [n]으로 팔아서 자금을 마련하세요.")
                continue
            
            gold -= cost
            print("강화 중..", end="", flush=True)
            for _ in range(3): time.sleep(0.3); print(".", end="", flush=True)
            
            if random.randint(1, 100) <= suc:
                lv += 1
                print(f"\n✨ 성공! [+{lv} {cur_w}]가 되었습니다!")
            else:
                if lv >= 7: # 7강부터 파괴 위험
                    if random.random() < 0.2:
                        print("\n💥 파괴됨! 무기가 가루가 되었습니다. (0강 초기화)"); lv = 0
                    else:
                        lv -= 1; print("\n❌ 실패! 레벨이 1 하락했습니다.")
                elif lv >= 3:
                    lv -= 1; print("\n❌ 실패! 레벨이 1 하락했습니다.")
                else:
                    print("\n❌ 실패! 다행히 레벨은 유지됐습니다.")

        elif cmd == 'n': # 판매 로직 (사냥 대신 돈 버는 법)
            gold += sell_val
            print(f"💰 [+{lv} {cur_w}]를 {sell_val}G에 팔았습니다. (무기 초기화)")
            lv = 0

        elif cmd == 'c': # 무기 교체 로직
            w_idx = (w_idx + 1) % len(weps)
            print(f"🔄 무기를 [{weps[w_idx]}]로 교체했습니다! (강화 수치 유지)")

        elif cmd == 'q':
            print(f"최종 자산 {gold}G를 남기고 종료합니다."); break
        else:
            print("명령어를 확인해주세요 (y, n, c, q)")

if __name__ == "__main__":
    game()
