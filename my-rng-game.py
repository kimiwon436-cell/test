import random, time

def game():
    lv, gold = 0, 1000  # 초기 자산 1,000G
    weps = ["단검", "장검", "엑스칼리버", "광선검", "죽창", "운석지팡이"]
    w_idx = 0
    
    print("\n" + "="*45)
    print("      🔥 전설의 대장장이: 강화 & 판매 🔥")
    print("="*45)

    while True:
        cur_w = weps[w_idx]
        cost = 100 + (lv * 100)  # 레벨업 비용
        sell_val = (lv * 250) + (lv**2 * 120) + 100  # 판매 시 받는 돈
        suc = max(5, 95 - (lv * 12))  # 확률 (높아질수록 급감)

        print(f"\n[현재 무기]: +{lv} {cur_w}")
        print(f"[보유 골드]: {gold:,.0f}G")
        print("-" * 45)
        # 명령어와 능력을 한눈에 보이게 출력
        print(f" (y) 강화: {cost}G 소모 / 성공확률 {suc}%")
        print(f" (n) 판매: 현재 무기를 팔아 {sell_val:,.0f}G 획득 (0강으로 초기화)")
        print(f" (c) 변경: 무기 스킨 바꾸기 (강화 수치는 그대로!)")
        print(f" (q) 종료: 게임을 마칩니다.")
        print("-" * 45)
        
        cmd = input("원하는 능력의 키를 입력하세요: ").lower()

        if cmd == 'y':
            if gold < cost:
                print("\n🚫 [잔액 부족] 무기를 팔아서 돈을 먼저 버세요!")
                continue
            gold -= cost
            print("🔨 망치질 중", end="", flush=True)
            for _ in range(3): time.sleep(0.3); print(".", end="", flush=True)
            
            if random.randint(1, 100) <= suc:
                lv += 1
                print(f"\n✨ 강화 성공! [+{lv} {cur_w}]가 되었습니다!")
            else:
                if lv >= 10: # 10강부터 파괴
                    print("\n💥 [파괴] 무기가 가루가 되었습니다! (0강 초기화)"); lv = 0
                elif lv >= 5: # 5강부터 하락
                    lv -= 1; print("\n❌ [실패] 단계가 미끄러졌습니다. (-1)")
                else:
                    print("\n❌ [실패] 강화에 실패했습니다.")

        elif cmd == 'n':
            gold += sell_val
            print(f"\n💰 [판매 완료] {sell_val:,.0f}G가 입금되었습니다!")
            lv = 0

        elif cmd == 'c':
            w_idx = (w_idx + 1) % len(weps)
            print(f"\n🔄 무기 모양을 [{weps[w_idx]}]로 바꿨습니다!")

        elif cmd == 'q':
            print(f"\n👋 최종 자산 {gold:,.0f}G를 챙겨서 떠납니다. 안녕히 가세요!")
            break
        else:
            print("\n⚠️ 잘못된 입력입니다. (y, n, c, q 중에서 골라주세요)")

if __name__ == "__main__":
    game()
