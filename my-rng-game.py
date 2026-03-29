import random
import time

def start_game():
    item_level = 0
    gold = 1000
    is_broken = False

    print("=== 🛠️ 본격 전설의 검 강화 노가다 ===\n")
    print("목표: +15강 검을 만들어 은퇴하세요!")
    print("주의: +6부터는 하락 위험, +11부터는 파괴 위험이 있습니다.")

    while not is_broken:
        print(f"\n[현재 상태] 아이템: +{item_level} 전설의 검 | 보유 골드: {gold}G")
        
        # 레벨별 강화 비용 및 성공 확률 설정
        cost = 100 + (item_level * 50)
        
        if item_level < 5: success_rate = 90 - (item_level * 10) # 1~5강: 90%~50%
        elif item_level < 10: success_rate = 40 - (item_level - 5) * 5 # 6~10강: 40%~20%
        else: success_rate = max(1, 15 - (item_level - 10) * 2) # 11강~: 15%~최소 1%

        print(f"강화 비용: {cost}G | 성공 확률: {success_rate}%")
        choice = input("강화하시겠습니까? (y/n / 종료: q): ").lower()

        if choice == 'q':
            print(f"\n최종 +{item_level}강에서 멈췄습니다. 수고하셨습니다!")
            break
        if choice != 'y': continue

        if gold < cost:
            print("❌ 골드가 부족합니다! 사냥(n)을 해서 돈을 벌어오세요.")
            action = input("사냥하러 갈까요? (y/n): ")
            if action == 'y':
                earned = random.randint(200, 500)
                gold += earned
                print(f"⚔️ 사냥 완료! {earned}G를 벌었습니다.")
            continue

        # 강화 진행
        gold -= cost
        print("강화 시도 중...", end="", flush=True)
        for _ in range(3):
            time.sleep(0.4)
            print(".", end="", flush=True)
        print()

        roll = random.randint(1, 100)
        if roll <= success_rate:
            item_level += 1
            print(f"✨ [성공] 아이템이 +{item_level}강이 되었습니다! ✨")
            if item_level >= 15:
                print("\n🎉 축하합니다! +15강 전설의 검을 완성하여 게임을 클리어했습니다! 🎉")
                break
        else:
            # 실패 패널티
            if item_level >= 10: # 10강 이상에서 실패 시 20% 확률로 파괴
                if random.random() < 0.2:
                    print("💥 [파괴] 아이템이 형체를 알아볼 수 없게 박살 났습니다... 게임 오버.")
                    is_broken = True
                else:
                    item_level -= 1
                    print(f"❌ [실패] 강화 실패! 단계가 미끄러져 +{item_level}이 되었습니다.")
            elif item_level >= 5: # 5강 이상에서 실패 시 단계 하락
                item_level -= 1
                print(f"❌ [실패] 강화 실패! 단계가 미끄러져 +{item_level}이 되었습니다.")
            else:
                print("❌ [실패] 강화에 실패했지만, 다행히 단계는 유지되었습니다.")

if __name__ == "__main__":
    start_game()
