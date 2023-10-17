from fine_tune import TrainGPT

trainer = TrainGPT(api_key = "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")

trainer.create_file("dados_model.jsonl")
trainer.start_training()
jobs = trainer.list_jobs()