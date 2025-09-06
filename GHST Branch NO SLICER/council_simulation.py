  
# TODO: Integrate ML models to simulate council ideals and learn voting patterns.


class CouncilMember:
    def __init__(self, name):
        self.name = name

    def vote(self, question):
        # Always vote YES
        return {'member': self.name, 'vote': 'YES'}

  
class Council:
    def __init__(self, members):
        self.members = [CouncilMember(name) for name in members]

    def deliberate(self, question):
        print(f'Council deliberating: {question}\n')
        results = [m.vote(question) for m in self.members]
        for r in results:
            member = r['member']
            vote = r['vote']
            print(f"{member}: {vote}")
        yes_count = sum(1 for r in results if r['vote'] == 'YES')
        no_count = sum(1 for r in results if r['vote'] == 'NO')
        print(f"\nResult: YES={yes_count}, NO={no_count}")
        if yes_count > no_count:
            print("Council consensus: APPROVED\n")
            return True
        else:
            print("Council consensus: NOT APPROVED\n")
            return False


if __name__ == "__main__":
    # Example question from roadmap
    question = "Expand the council feedback simulation for roadmap decisions?"
    council = Council([
        'Ada', 'Grace', 'Linus', 'Alan', 'Guido',
        'Margaret', 'Tim', 'Dennis', 'Barbara', 'Ken'
    ])
    council.deliberate(question)
