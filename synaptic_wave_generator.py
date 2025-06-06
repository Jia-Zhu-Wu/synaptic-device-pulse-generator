# -*- coding: utf-8 -*-
import customtkinter as ctk
import pandas as pd
import webbrowser
from PIL import Image
import sys
import os

def resource_path(relative_path):
    """取得打包後與開發時的正確資源路徑"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class WaveGeneratorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Synaptic Wave Generator")
        self.geometry("700x730")
        self.resizable(False, False)
        self.all_cycles = []

        # ====== 開頭設定 Frame ======
        open_frame = ctk.CTkFrame(self)
        open_frame.pack(pady=(12, 4), padx=12, fill="x")

        ctk.CTkLabel(open_frame, text="開頭數字（預設0）:").grid(row=0, column=0, sticky="w", padx=4, pady=2)
        self.opening_number_entry = ctk.CTkEntry(open_frame, placeholder_text="0", width=90)
        self.opening_number_entry.grid(row=0, column=1, padx=4, pady=2)
        ctk.CTkLabel(open_frame, text="連續次數（預設10000）:").grid(row=0, column=2, sticky="w", padx=4, pady=2)
        self.opening_zeros_entry = ctk.CTkEntry(open_frame, placeholder_text="10000", width=90)
        self.opening_zeros_entry.grid(row=0, column=3, padx=4, pady=2)

        # ====== 週期設定 Frame ======
        cycle_frame = ctk.CTkFrame(self)
        cycle_frame.pack(pady=(8, 2), padx=12, fill="x")

        ctk.CTkLabel(cycle_frame, text="--- 新增脈衝週期 ---").grid(row=0, column=0, columnspan=8, pady=(2, 2))
        ctk.CTkLabel(cycle_frame, text="脈衝振幅").grid(row=1, column=0, padx=2)
        self.wave_number_entry = ctk.CTkEntry(cycle_frame, placeholder_text="數值，可小數", width=70)
        self.wave_number_entry.grid(row=1, column=1, padx=2)
        ctk.CTkLabel(cycle_frame, text="持續次數").grid(row=1, column=2, padx=2)
        self.duration_entry = ctk.CTkEntry(cycle_frame, placeholder_text="正整數", width=70)
        self.duration_entry.grid(row=1, column=3, padx=2)
        ctk.CTkLabel(cycle_frame, text="間隔數值").grid(row=1, column=4, padx=2)
        self.interval_entry = ctk.CTkEntry(cycle_frame, placeholder_text="數值，可小數", width=70)
        self.interval_entry.grid(row=1, column=5, padx=2)
        ctk.CTkLabel(cycle_frame, text="間隔長度").grid(row=1, column=6, padx=2)
        self.interval_duration_entry = ctk.CTkEntry(cycle_frame, placeholder_text="正整數", width=70)
        self.interval_duration_entry.grid(row=1, column=7, padx=2)

        ctk.CTkLabel(cycle_frame, text="重複次數").grid(row=2, column=0, padx=2, pady=(2, 1))
        self.repeat_entry = ctk.CTkEntry(cycle_frame, placeholder_text="正整數", width=70)
        self.repeat_entry.grid(row=2, column=1, padx=2, pady=(2, 1))
        self.add_cycle_btn = ctk.CTkButton(cycle_frame, text="加入此脈衝週期", width=120, command=self.add_cycle)
        self.add_cycle_btn.grid(row=2, column=2, columnspan=6, padx=2, pady=(2, 1), sticky="w")

        self.cycle_list_label = ctk.CTkLabel(cycle_frame, text="目前已加入脈衝週期：0")
        self.cycle_list_label.grid(row=3, column=0, columnspan=8, sticky="w", pady=(2,0))
        self.cycle_history_box = ctk.CTkTextbox(cycle_frame, width=620, height=90, font=("Microsoft JhengHei", 12))
        self.cycle_history_box.grid(row=4, column=0, columnspan=8, padx=4, pady=(2,2))
        self.cycle_history_box.insert("end", "尚未加入任何脈衝週期...\n")
        self.cycle_history_box.configure(state="disabled")

        # ====== 刪除/清除 Frame ======
        delete_frame = ctk.CTkFrame(self)
        delete_frame.pack(pady=(5,2), padx=12, fill="x")
        ctk.CTkLabel(delete_frame, text="--- 刪除週期 ---").grid(row=0, column=0, columnspan=4)
        ctk.CTkLabel(delete_frame, text="編號:").grid(row=1, column=0, padx=2)
        self.delete_index_entry = ctk.CTkEntry(delete_frame, width=60, placeholder_text="輸入編號")
        self.delete_index_entry.grid(row=1, column=1, padx=2)
        self.delete_btn = ctk.CTkButton(delete_frame, text="刪除此波型", width=80, command=self.delete_one_cycle)
        self.delete_btn.grid(row=1, column=2, padx=2)
        self.clear_btn = ctk.CTkButton(delete_frame, text="全部清除", width=80, command=self.clear_cycles)
        self.clear_btn.grid(row=1, column=3, padx=2)

        # ====== 結尾/輸出 Frame ======
        end_frame = ctk.CTkFrame(self)
        end_frame.pack(pady=(10,2), padx=12, fill="x")

        ctk.CTkLabel(end_frame, text="結尾個數（預設0）:").grid(row=0, column=0, padx=4)
        self.ending_count_entry = ctk.CTkEntry(end_frame, placeholder_text="0", width=90)
        self.ending_count_entry.grid(row=0, column=1, padx=2)
        ctk.CTkLabel(end_frame, text="（若開頭非0，結尾自動與開頭同步）").grid(row=0, column=2, padx=4)
        ctk.CTkLabel(end_frame, text="輸出檔名（預設output.csv）:").grid(row=1, column=0, padx=4)
        self.output_file_entry = ctk.CTkEntry(end_frame, placeholder_text="output.csv", width=120)
        self.output_file_entry.grid(row=1, column=1, padx=2)

        self.generate_btn = ctk.CTkButton(end_frame, text="產生CSV", width=100, command=self.generate_csv)
        self.generate_btn.grid(row=2, column=0, columnspan=4, pady=(10, 2))

        self.result_label = ctk.CTkLabel(end_frame, text="")
        self.result_label.grid(row=3, column=0, columnspan=4, pady=(2, 2))

        # ====== GitHub icon 按鈕（放最下方）======
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(side="bottom", pady=8)
        github_img_path = resource_path("github.png")
        github_img = ctk.CTkImage(light_image=Image.open(github_img_path), size=(83, 48))
        self.github_btn = ctk.CTkButton(
            bottom_frame, image=github_img, text="", width=36, height=36,
            fg_color="transparent", hover_color="#e1e1e1", command=self.open_github, border_width=0
        )
        self.github_btn.pack()

    def open_github(self):
        # 改成你的 GitHub 倉庫網址
        webbrowser.open("https://github.com/Jia-Zhu-Wu/synaptic-device-pulse-generator")

    def add_cycle(self):
        try:
            wave_number = float(self.wave_number_entry.get())
            duration = int(self.duration_entry.get())
            interval = float(self.interval_entry.get())
            interval_duration = int(self.interval_duration_entry.get())
            repeat = int(self.repeat_entry.get())
            if not (duration > 0 and interval_duration >= 0 and repeat > 0):
                raise ValueError
        except:
            self.result_label.configure(text="請正確填寫波型參數！", text_color="red")
            return
        self.all_cycles.append((wave_number, duration, interval, interval_duration, repeat))
        self.cycle_list_label.configure(
            text=f"目前已加入波型週期：{len(self.all_cycles)}"
        )
        self.show_cycle_history()
        self.wave_number_entry.delete(0, 'end')
        self.duration_entry.delete(0, 'end')
        self.interval_entry.delete(0, 'end')
        self.interval_duration_entry.delete(0, 'end')
        self.repeat_entry.delete(0, 'end')
        self.result_label.configure(text="已加入此波型週期！", text_color="green")

    def show_cycle_history(self):
        self.cycle_history_box.configure(state="normal")
        self.cycle_history_box.delete("1.0", "end")
        if not self.all_cycles:
            self.cycle_history_box.insert("end", "尚未加入任何週期...\n")
        else:
            for idx, (w, d, i, idur, r) in enumerate(self.all_cycles, 1):
                self.cycle_history_box.insert(
                    "end", f"週期{idx}：數字{w}，持續{d}，間隔值{i}，間隔長度{idur}，重複{r}\n"
                )
        self.cycle_history_box.configure(state="disabled")

    def delete_one_cycle(self):
        try:
            idx = int(self.delete_index_entry.get())
            if not (1 <= idx <= len(self.all_cycles)):
                raise ValueError
            self.all_cycles.pop(idx - 1)
            self.result_label.configure(text=f"已刪除週期{idx}", text_color="orange")
            self.show_cycle_history()
            self.cycle_list_label.configure(
                text=f"目前已加入波型週期：{len(self.all_cycles)}"
            )
        except:
            self.result_label.configure(text="請輸入有效的週期編號", text_color="red")
        self.delete_index_entry.delete(0, 'end')

    def clear_cycles(self):
        self.all_cycles = []
        self.show_cycle_history()
        self.cycle_list_label.configure(
            text=f"目前已加入波型週期：0"
        )
        self.result_label.configure(text="已全部清除！", text_color="orange")

    def generate_csv(self):
        try:
            opening_number = float(self.opening_number_entry.get()) if self.opening_number_entry.get() else 0
        except:
            self.result_label.configure(text="開頭數字格式錯誤", text_color="red")
            return
        try:
            opening_zeros = int(self.opening_zeros_entry.get()) if self.opening_zeros_entry.get() else 10000
            assert opening_zeros > 0
        except:
            self.result_label.configure(text="開頭數字連續次數錯誤", text_color="red")
            return
        if len(self.all_cycles) == 0:
            self.result_label.configure(text="請至少加入一個波型週期", text_color="red")
            return
        all_data = [opening_number] * opening_zeros
        for wave_number, duration, interval, interval_duration, repeat in self.all_cycles:
            one_cycle = [wave_number] * duration + [interval] * interval_duration
            all_data += one_cycle * repeat

        # 新增：結尾自動與開頭同步
        try:
            ending_count = int(self.ending_count_entry.get()) if self.ending_count_entry.get() else 0
            assert ending_count >= 0
        except:
            self.result_label.configure(text="結尾個數錯誤", text_color="red")
            return
        ending_value = opening_number if opening_number != 0 else 0
        all_data += [ending_value] * ending_count

        output_file = self.output_file_entry.get().strip() or "output.csv"
        df = pd.DataFrame(all_data)
        try:
            df.to_csv(output_file, index=False, header=False)
            self.result_label.configure(
                text=f"CSV檔案產生完成！({output_file})", text_color="green"
            )
        except Exception as e:
            self.result_label.configure(
                text=f"存檔失敗：{e}", text_color="red"
            )

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    app = WaveGeneratorGUI()
    app.mainloop()
