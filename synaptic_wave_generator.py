# -*- coding: utf-8 -*-
"""
Created on Mon May 26 13:17:37 2025

@author: user
"""

import customtkinter as ctk
import pandas as pd

class WaveGeneratorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Synaptic Wave Generator")
        self.geometry("480x800")
        self.resizable(False, False)
        self.all_cycles = []

        # 開頭零
        self.opening_zeros_label = ctk.CTkLabel(self, text="開頭零數量（預設10000）:")
        self.opening_zeros_label.pack(pady=(15, 0))
        self.opening_zeros_entry = ctk.CTkEntry(self, placeholder_text="10000")
        self.opening_zeros_entry.pack()

        # 波型參數
        self.cycle_title = ctk.CTkLabel(self, text="--- 新增波型週期 ---")
        self.cycle_title.pack(pady=(30, 0))
        self.wave_number_entry = ctk.CTkEntry(self, placeholder_text="方波數字(0~9)")
        self.wave_number_entry.pack(pady=(8, 0))
        self.duration_entry = ctk.CTkEntry(self, placeholder_text="方波持續次數（正整數）")
        self.duration_entry.pack(pady=(8, 0))
        self.interval_entry = ctk.CTkEntry(self, placeholder_text="間隔零數量（>=0）")
        self.interval_entry.pack(pady=(8, 0))
        self.repeat_entry = ctk.CTkEntry(self, placeholder_text="週期重複次數（正整數）")
        self.repeat_entry.pack(pady=(8, 0))
        self.add_cycle_btn = ctk.CTkButton(self, text="加入此波型週期", command=self.add_cycle)
        self.add_cycle_btn.pack(pady=(15, 5))

        # 顯示所有加入的週期
        self.cycle_list_label = ctk.CTkLabel(self, text="目前已加入波型週期：0")
        self.cycle_list_label.pack()
        self.cycle_history_box = ctk.CTkTextbox(self, width=430, height=180, font=("Microsoft JhengHei", 13))
        self.cycle_history_box.pack(pady=(5, 0))
        self.cycle_history_box.insert("end", "尚未加入任何週期...\n")
        self.cycle_history_box.configure(state="disabled")  # 只讀

        # --- 新增刪除週期的區域 ---
        self.delete_title = ctk.CTkLabel(self, text="--- 刪除週期 ---")
        self.delete_title.pack(pady=(18, 0))
        delete_frame = ctk.CTkFrame(self)
        delete_frame.pack(pady=(3, 0))
        self.delete_index_entry = ctk.CTkEntry(delete_frame, width=80, placeholder_text="輸入編號")
        self.delete_index_entry.pack(side="left", padx=(5, 5))
        self.delete_btn = ctk.CTkButton(delete_frame, text="刪除此週期", width=90, command=self.delete_one_cycle)
        self.delete_btn.pack(side="left", padx=(2, 5))
        self.clear_btn = ctk.CTkButton(delete_frame, text="全部清除", width=90, command=self.clear_cycles)
        self.clear_btn.pack(side="left", padx=(2, 5))

        # 結尾零
        self.ending_zeros_label = ctk.CTkLabel(self, text="結尾零數量（預設0）:")
        self.ending_zeros_label.pack(pady=(30, 0))
        self.ending_zeros_entry = ctk.CTkEntry(self, placeholder_text="0")
        self.ending_zeros_entry.pack()

        # 輸出檔名
        self.output_file_label = ctk.CTkLabel(self, text="輸出檔名（預設 output.csv）:")
        self.output_file_label.pack(pady=(30, 0))
        self.output_file_entry = ctk.CTkEntry(self, placeholder_text="output.csv")
        self.output_file_entry.pack()

        # 產生CSV 按鈕
        self.generate_btn = ctk.CTkButton(self, text="產生CSV", command=self.generate_csv)
        self.generate_btn.pack(pady=(25, 10))

        # 訊息提示
        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.pack()

    def add_cycle(self):
        try:
            wave_number = int(self.wave_number_entry.get())
            duration = int(self.duration_entry.get())
            interval = int(self.interval_entry.get())
            repeat = int(self.repeat_entry.get())
            if not (0 <= wave_number <= 9 and duration > 0 and interval >= 0 and repeat > 0):
                raise ValueError
        except:
            self.result_label.configure(text="請正確填寫波型參數！", text_color="red")
            return
        self.all_cycles.append((wave_number, duration, interval, repeat))
        self.cycle_list_label.configure(
            text=f"目前已加入波型週期：{len(self.all_cycles)}"
        )
        # 更新顯示
        self.show_cycle_history()
        # 清空欄位
        self.wave_number_entry.delete(0, 'end')
        self.duration_entry.delete(0, 'end')
        self.interval_entry.delete(0, 'end')
        self.repeat_entry.delete(0, 'end')
        self.result_label.configure(text="已加入此波型週期！", text_color="green")

    def show_cycle_history(self):
        self.cycle_history_box.configure(state="normal")
        self.cycle_history_box.delete("1.0", "end")
        if not self.all_cycles:
            self.cycle_history_box.insert("end", "尚未加入任何週期...\n")
        else:
            for idx, (w, d, i, r) in enumerate(self.all_cycles, 1):
                self.cycle_history_box.insert(
                    "end", f"週期{idx}：數字{w}，持續{d}，間隔{i}，重複{r}\n"
                )
        self.cycle_history_box.configure(state="disabled")

    def delete_one_cycle(self):
        try:
            idx = int(self.delete_index_entry.get())
            if not (1 <= idx <= len(self.all_cycles)):
                raise ValueError
            removed = self.all_cycles.pop(idx - 1)
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
            opening_zeros = int(self.opening_zeros_entry.get()) if self.opening_zeros_entry.get() else 10000
            assert opening_zeros > 0
        except:
            self.result_label.configure(text="開頭零數量錯誤", text_color="red")
            return
        if len(self.all_cycles) == 0:
            self.result_label.configure(text="請至少加入一個波型週期", text_color="red")
            return
        all_data = [0] * opening_zeros
        for wave_number, duration, interval, repeat in self.all_cycles:
            one_cycle = [wave_number] * duration + [0] * interval
            all_data += one_cycle * repeat
        try:
            ending_zeros = int(self.ending_zeros_entry.get()) if self.ending_zeros_entry.get() else 0
            assert ending_zeros >= 0
        except:
            self.result_label.configure(text="結尾零數量錯誤", text_color="red")
            return
        all_data += [0] * ending_zeros
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
