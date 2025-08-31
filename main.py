"""
Agentic Chunking 메인 실행 파일 - 한글 예시 버전
"""
from agentic_chunker import AgenticChunker
import config

def main():
    """메인 실행 함수"""
    print("🚀 Agentic Chunking Test Started\n")
    
    # 한글 텍스트에서 자동으로 명제 추출 및 청킹
    print("📝 한글 텍스트를 이용한 Agentic Chunking 테스트\n")
    
    # 더 길고 다양한 주제의 한글 텍스트
    korean_text = """
    인공지능은 현재 우리 사회의 모든 분야에서 혁신을 이끌고 있습니다. 
    머신러닝 알고리즘은 대량의 데이터를 처리하고 인간이 놓칠 수 있는 패턴을 찾아냅니다. 
    딥러닝은 머신러닝의 한 분야로, 다층 신경망을 사용하여 복잡한 문제를 해결합니다. 
    자연어 처리 기술은 컴퓨터가 인간의 언어를 이해하고 생성할 수 있게 합니다.
    컴퓨터 비전은 기계가 시각적 정보를 해석하고 분석할 수 있도록 합니다.
    
    기후 변화는 21세기 인류가 직면한 가장 심각한 문제 중 하나입니다.
    지구 온난화로 인해 빙하가 녹고 해수면이 상승하고 있습니다.
    극한 기상 현상이 더욱 빈번하고 강력해지고 있습니다.
    태양광과 풍력 같은 재생 에너지가 점점 더 경제적이 되고 있습니다.
    전 세계가 탄소 중립을 위해 노력하고 있습니다.
    
    한국의 전통 음식은 세계적으로 인기를 얻고 있습니다.
    김치는 한국을 대표하는 발효 음식으로 건강에 매우 좋습니다.
    불고기와 갈비는 외국인들이 가장 좋아하는 한국 요리입니다.
    비빔밥은 다양한 채소와 고추장이 어우러진 건강한 한 그릇 요리입니다.
    한식의 특징은 발효 음식과 다양한 반찬 문화입니다.
    
    우주 탐사는 인류의 오랜 꿈이었습니다.
    NASA는 2024년 달 착륙을 목표로 아르테미스 프로그램을 진행하고 있습니다.
    화성 탐사는 인류의 다음 목표로 여러 국가가 참여하고 있습니다.
    우주 정거장에서는 무중력 환경을 이용한 다양한 실험이 진행됩니다.
    민간 우주 기업들도 우주 관광과 화물 운송에 참여하고 있습니다.
    
    교육 시스템은 디지털 시대에 맞춰 변화하고 있습니다.
    온라인 학습 플랫폼이 전통적인 교실 수업을 보완하고 있습니다.
    개인 맞춤형 학습이 AI 기술을 통해 가능해지고 있습니다.
    코딩 교육이 초등학교부터 필수 과목으로 도입되고 있습니다.
    평생 학습의 중요성이 강조되면서 성인 교육 시장이 확대되고 있습니다.
    
    건강한 생활습관은 현대인에게 필수적입니다.
    규칙적인 운동은 신체적, 정신적 건강을 모두 개선시킵니다.
    균형 잡힌 식단은 각종 질병을 예방하는 데 중요한 역할을 합니다.
    충분한 수면은 면역력 강화와 스트레스 해소에 도움이 됩니다.
    명상과 요가 같은 마음챙김 활동이 정신 건강에 도움이 됩니다.
    
    경제학에서 공급과 수요의 법칙은 시장 경제의 기본 원리입니다.
    인플레이션은 화폐 가치 하락으로 물가가 지속적으로 상승하는 현상입니다.
    중앙은행은 금리 정책을 통해 경제 안정을 도모합니다.
    글로벌 경제는 각국의 경제가 서로 밀접하게 연결되어 있습니다.
    디지털 화폐와 블록체인 기술이 금융 시스템을 변화시키고 있습니다.
    """
    
    # AgenticChunker 초기화
    ac = AgenticChunker()
    
    # 텍스트에서 명제 추출
    print("🔍 한글 텍스트에서 명제 추출 중...")
    extracted_propositions = ac.extract_propositions_from_text(korean_text)
    
    print(f"\n📋 추출된 명제 개수: {len(extracted_propositions)}")
    print("=" * 60)
    for i, prop in enumerate(extracted_propositions, 1):
        print(f"   {i:2d}. {prop}")
    
    print("\n" + "=" * 80)
    print("🔄 추출된 명제들을 청크로 분류 중...")
    print("=" * 80)
    
    # 추출된 명제들을 처리
    ac.add_propositions(extracted_propositions)
    
    # 결과 출력
    ac.print_chunks()
    
    # 추가 분석 정보
    print("\n" + "🔍 청킹 결과 분석")
    print("=" * 80)
    
    chunks = ac.get_chunks()
    total_propositions = sum(len(chunk['propositions']) for chunk in chunks.values())
    
    print(f"📊 전체 통계:")
    print(f"   • 총 청크 수: {len(chunks)}개")
    print(f"   • 총 명제 수: {total_propositions}개")
    print(f"   • 평균 청크당 명제 수: {total_propositions/len(chunks):.1f}개")
    
    print(f"\n📈 각 청크별 명제 수:")
    for i, (chunk_id, chunk_data) in enumerate(chunks.items(), 1):
        prop_count = len(chunk_data['propositions'])
        title = chunk_data['title']
        print(f"   청크 {i}: {prop_count}개 명제 - \"{title}\"")
    
    print(f"\n✅ Agentic Chunking 완료!")
    print(f"   관련성 있는 내용들이 {len(chunks)}개의 의미 있는 그룹으로 분류되었습니다.")

if __name__ == "__main__":
    main()
