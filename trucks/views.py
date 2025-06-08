from django.shortcuts import render
from django.contrib import messages
from django.contrib.gis.geos import Point
from .models import Truck, Stock
from .forms import UnloadForm


def unload_view(request):
    trucks = Truck.objects.all()
    stock = Stock.objects.first()

    if not stock:
        messages.error(request, "Не найден склад для разгрузки. Сначала создайте склад в админке.")
        return render(request, "unload.html", {"trucks": trucks})

    # Всегда берем исходные значения из базы данных
    original_stock = Stock.objects.get(pk=stock.pk)
    volume_before = original_stock.volume
    sio2_before = original_stock.sio2
    fe_before = original_stock.fe

    if request.method == "POST":
        form = UnloadForm(trucks, request.POST)
        if form.is_valid():
            try:
                # Создаем временные переменные для расчета
                temp_volume = original_stock.volume
                temp_sio2 = original_stock.sio2 * original_stock.volume
                temp_fe = original_stock.fe * original_stock.volume

                unloaded_trucks = []
                errors = []
                updated_trucks = []

                for truck in trucks:
                    coord_raw = form.cleaned_data.get(f'coord_{truck.id}')
                    try:
                        x_str, y_str = coord_raw.strip().split()
                        point = Point(float(x_str), float(y_str))

                        if original_stock.area.contains(point):
                            # Добавляем к временным значениям
                            temp_volume += truck.current_load
                            temp_sio2 += truck.sio2 * truck.current_load
                            temp_fe += truck.fe * truck.current_load
                            unloaded_trucks.append(truck.board_number)

                            # Помечаем самосвал для обновления (обнуления груза)
                            updated_trucks.append(truck)
                        else:
                            errors.append(f"Координаты вне территории склада для самосвала {truck.board_number}")
                    except (ValueError, AttributeError) as e:
                        errors.append(f"Ошибка в координатах для самосвала {truck.board_number}: {e}")

                # Обновляем склад только если были успешные разгрузки
                if unloaded_trucks:
                    # Рассчитываем новые проценты
                    new_sio2 = (temp_sio2 / temp_volume) if temp_volume else 0
                    new_fe = (temp_fe / temp_volume) if temp_volume else 0

                    # Обновляем склад
                    stock.volume = temp_volume
                    stock.sio2 = new_sio2
                    stock.fe = new_fe
                    stock.save()

                    # Обнуляем груз у разгруженных самосвалов
                    for truck in updated_trucks:
                        truck.current_load = 0
                        truck.save()

                    messages.success(request, f"Успешно разгружены самосвалы: {', '.join(unloaded_trucks)}")

                for error in errors:
                    messages.error(request, error)

            except Exception as e:
                messages.error(request, f"Ошибка при разгрузке: {e}")
    else:
        form = UnloadForm(trucks)

    # Всегда показываем актуальные данные из базы
    current_stock = Stock.objects.get(pk=stock.pk)
    return render(request, "unload.html", {
        "form": form,
        "trucks": trucks,
        "stock": current_stock,
        "volume_before": volume_before,
        "sio2_before": sio2_before,
        "fe_before": fe_before
    })