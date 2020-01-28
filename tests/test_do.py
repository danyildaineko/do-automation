#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time

import allure
import pytest
import logging

from blocks.main import MainPage


class TestFunctionality:
    @pytest.mark.debug
    @allure.title('Проверка блокировки видео канала если аудио при проверке было недоступно')
    @allure.severity(allure.severity_level.NORMAL)
    def test_off_video_if_audio_block(self, driver):
        main = MainPage(driver)
        main.start_work_day(is_video = True, is_audio = False)

        assert main.verify_video_active()

    @allure.title('Проверяет что удаленные симптомы не влияют на предлогаемые диагнозы')
    @allure.severity(allure.severity_level.MINOR)
    def test_cancel_symptom_no_conclusion(self, driver):
        main = MainPage(driver)
        main.select_request(number = 0)
        main.add_symptom('тошнота')
        main.delete_symptom(symptom = 'тошнота')

        assert main.verify_no_conclusion()

    @pytest.mark.debug
    @allure.title('Проверка смены состояние иконок прогресса после заполнения данных в обращении')
    @allure.severity(allure.severity_level.NORMAL)
    def test_progress_bar(self, driver):
        main = MainPage(driver)
        main.select_request(number = 5)
        main.add_conclusion('Геморрой')
        main.add_analysis('Анализ')
        main.add_symptom('Тошнота')
        main.add_drug('Препарат')

        assert main.is_indicator_symptomes() and main.is_indicator_diagnosis() and main.is_indicator_analysis() and main.is_indicator_drug()

    @allure.title('Проверка соответствия подтвержденного диагноза названию этого обращения')
    @allure.severity(allure.severity_level.NORMAL)
    def test_selected_conclusion_in_request_title(self, driver):
        main = MainPage(driver)
        main.select_request(number = 3)
        main.add_conclusion('Диарея')
        result = main.current_request_name()
        main.clear_conclusions()

        assert "Диарея" in result


class TestUI:
    @allure.title('Проверка отображения ошибки при попытке сохранить обращение без заполненных данных')
    @allure.severity(allure.severity_level.NORMAL)
    def test_error_save_appointment_without_data(self, driver):
        main = MainPage(driver)
        main.select_request(6)
        main.save_appointment()

        assert main.is_present_save_error()

    @allure.title('Проверка отображения ошибки при попытке выйти из аккаунта с не завершенными обращениями')
    @allure.severity(allure.severity_level.NORMAL)
    def test_error_logout_with_requests(self, driver):
        main = MainPage(driver)
        main.logout()

        assert main.is_present_logout_error()

    @allure.title('Проверка блокировки остальных диагнозов в списке после подтверждения конкретного диагноза')
    @allure.severity(allure.severity_level.NORMAL)
    def test_block_conclusions_after_select(self, driver):
        main = MainPage(driver)
        main.select_request(1)
        main.add_symptom("Тошнота")
        main.add_conclusion("Целиакия")

        assert main.verify_block_conclusions()

    @allure.title('Проверка отображения подтвержденного диагноза на первом месте в списке')
    @allure.severity(allure.severity_level.MINOR)
    def test_selected_conclusion_in_first_row(self, driver):
        conclusion = "Целиакия"

        main = MainPage(driver)
        main.select_request(3)
        main.add_symptom("Тошнота")
        main.add_conclusion(conclusion)
        position = main.get_conclusion_position(conclusion)
        main.deactivate_conclusion()
        assert position == 1
    
    @allure.title('Проверка возвращения отмененного диагноза на свою позицую в списке')
    @allure.severity(allure.severity_level.MINOR)
    def test_canceled_conclusion_return_to_own_position(self, driver):
        conclusion = "Целиакия"

        main = MainPage(driver)
        main.select_request(3)
        main.add_symptom("Тошнота")
        position = main.get_conclusion_position(conclusion)
        main.add_conclusion(conclusion)
        main.deactivate_conclusion()
        
        assert position == main.get_conclusion_position(conclusion)

    @allure.title('Проверка разблокировки диагнозов в списке после отменения подтвержденного диагноза')
    @allure.severity(allure.severity_level.MINOR)
    def test_unlocking_all_conclusions_after_cancel_selected(self, driver):
        conclusion = "Целиакия"
        
        main = MainPage(driver)
        main.select_request(7)
        main.add_symptom("Тошнота")
        main.add_conclusion(conclusion)
        main.deactivate_conclusion()

        assert not main.verify_block_conclusions()

    # verify test validation of preparatov
