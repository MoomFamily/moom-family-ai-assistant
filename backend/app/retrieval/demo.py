DOCS=[('planning','A good project plan defines objectives, scope, milestones, responsibilities, dependencies and risks.'),('documentation','Technical documentation should explain installation, configuration, usage, architecture and troubleshooting.'),('meetings','An effective meeting has a clear objective, agenda, decisions and assigned action items.')]
def search(query: str) -> list[str]:
    terms=set(query.lower().split())
    ranked=sorted(DOCS,key=lambda d:len(terms & set(d[1].lower().split())),reverse=True)
    return [f'{name}: {body}' for name,body in ranked[:2] if terms & set(body.lower().split())]
