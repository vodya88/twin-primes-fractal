import numpy as np
import matplotlib.pyplot as plt
import time

def fast_god_sieve(limit):
    """
    Бронированное векторизованное решето Эратосфена.
    Работает на чистой векторной логике NumPy, исключающей ошибки типов.
    """
    print(f"\n[GOD MODE] Запуск ультимативного расчета до {limit:,}...")
    start_time = time.time()
    
    # Шаг 1. Находим базовые простые числа для фильтрации
    seg_size = int(np.sqrt(limit)) + 1
    base_sieve = np.ones(seg_size, dtype=bool)
    base_sieve[0:2] = False
    for i in range(2, int(np.sqrt(seg_size)) + 1):
        if base_sieve[i]:
            base_sieve[i*i::i] = False
    base_primes = np.where(base_sieve)[0]
    
    all_primes_list = []
    
    # Шаг 2. Поблочный расчет всей числовой оси
    for low in range(0, limit + 1, seg_size):
        high = min(low + seg_size - 1, limit)
        seg_sieve = np.ones(high - low + 1, dtype=bool)
        if low == 0:
            seg_sieve[0:2] = False
            
        for p in base_primes:
            start = max(p * p, ((low + p - 1) // p) * p)
            if start <= high:
                seg_sieve[start - low::p] = False
                
        seg_primes = np.where(seg_sieve)[0] + low
        if len(seg_primes) > 0:
            all_primes_list.append(seg_primes)
            
    # Соединяем все найденные простые числа в один монолитный массив
    print("[GOD MODE] Сборка числовой оси...")
    all_primes = np.concatenate(all_primes_list)
    
    # Шаг 3. Векторный поиск близнецов
    print("[GOD MODE] Выделение пар близнецов...")
    diffs = np.diff(all_primes)
    twin_mask_left = (diffs == 2)
    
    left_twins = all_primes[:-1][twin_mask_left]
    right_twins = all_primes[1:][twin_mask_left]
    
    final_twins = np.empty(2 * len(left_twins), dtype=np.int64)
    final_twins[0::2] = left_twins
    final_twins[1::2] = right_twins
    
    print(f"[GOD MODE] Векторный расчет успешно завершен за {time.time() - start_time:.2f} сек.!")
    return final_twins

def calculate_fractal_dimension_fast(twins, limit):
    """Быстрый логарифмический Box-Counting с исправленным выводом коэффициентов"""
    if len(twins) < 2: return 0.0
    scales = np.logspace(2, int(np.log10(limit)) - 1, num=8)
    counts = []
    for scale in scales:
        boxes = np.unique((twins / scale).astype(np.int64))
        counts.append(len(boxes))
    coeffs = np.polyfit(np.log(1 / scales), np.log(counts), 1)
    return float(coeffs[0])  # Исправлено: берем строго первый коэффициент (наклон D)

def plot_god_galaxy(limit):
    try:
        twins = fast_god_sieve(limit)
        D_twins = calculate_fractal_dimension_fast(twins, limit)
        total_pairs = len(twins) // 2
        
        print(f"\n[УСПЕХ] Математический барьер в 1 МИЛЛИАРД взломан!")
        print(f"[УСПЕХ] Глобальная размерность Хаусдорфа D = {D_twins:.4f}")
        print(f"[УСПЕХ] Всего пар-близнецов найдено: {total_pairs:,}")
        
        # Умное прореживание 1:150 для потрясающей, сочной детализации узора
        thinned = twins[::150]
        
        # Логарифмический масштаб радиуса для красивой панорамы центра
        theta = thinned
        r = np.log(thinned) 
        
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(11, 11), subplot_kw={'projection': 'polar'})
        
        try:
            mng = plt.get_current_fig_manager()
            mng.window.state('zoomed')
        except:
            pass

        # Рисуем звездное неоновое облако миллиарда чисел
        ax.scatter(theta, r, color='magenta', s=1.0, alpha=0.6, edgecolors='none', label='Twin Primes Dust')
        
        title_text = (
            f"THE GOD GALAXY: 1 BILLION NUMBER SCALE (Logarithmic Radius)\n"
            f"Global Stable Hausdorff Dimension D = {D_twins:.4f}\n"
            f"Total Twin Pairs Found: {total_pairs:,}"
        )
        ax.set_title(title_text, fontsize=12, color='lime', fontweight='bold', pad=35)
        
        ax.set_rticks([]) 
        ax.set_thetagrids([])
        ax.spines['polar'].set_visible(False)
        ax.legend(loc='upper right', frameon=True, facecolor='black', edgecolor='gray')
        
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"\n[ОШИБКА ГРАФИКА]: {e}")
        
    input("\nНажмите Enter, чтобы закрыть программу...")

if __name__ == "__main__":
    GOD_LIMIT = 1000000000 
    plot_god_galaxy(GOD_LIMIT)
