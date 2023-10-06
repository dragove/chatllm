from transformers import AutoTokenizer, AutoModelForCausalLM

# CPU 用户请使用以下代码
# tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-7B-Chat-Int4",
#                                           trust_remote_code=True)
# model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-7B-Chat-Int4",
#                                              device_map="cpu",
#                                              trust_remote_code=True)
# GPU 用户请使用以下代码
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-7B-Chat-Int4",
                                          trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-7B-Chat-Int4",
                                             device_map="cuda",
                                             trust_remote_code=True)


model = model.eval()


def chat(prompt, history=[]):
    res, his = model.chat(tokenizer, prompt, history)
    return res, his


def print_chat(prompt, history=[]):
    print(f"Q: {prompt}\n")
    response = chat(prompt, history)[0]
    print(f"A: {response}\n")
    return response
    

if __name__ == "__main__":
    print_chat("你好")
