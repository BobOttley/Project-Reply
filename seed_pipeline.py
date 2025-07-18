from models import Session, PipelineStage

def seed_pipeline_stages():
    stages = ["New", "Contacted", "Tour Booked", "Applied", "Enrolled"]
    session = Session()
    for stage in stages:
        exists = session.query(PipelineStage).filter_by(name=stage).first()
        if not exists:
            session.add(PipelineStage(name=stage))
    session.commit()
    session.close()
    print("Pipeline stages seeded.")

if __name__ == "__main__":
    seed_pipeline_stages()
