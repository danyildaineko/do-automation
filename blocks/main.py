#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import time

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from blocks.base_page import BasePage


class MainPage(BasePage):
    """LOGIN PAGE"""
    COUNTRY_SELECTOR = (By.CSS_SELECTOR, 'app-select-countries')
    # For shadow elements
    shadow_COUNTRY_SEARCH = 'app-select-countries'
    shadow_SEARCH_COUNTRY = 'div.form-search input.form-control'
    shadow_COUNTRY_IN_LIST = 'div.item-country'
    COUNTRY_SEARCH = (By.CSS_SELECTOR, 'div.form-search input.form-control')
    COUNTRY_IN_LIST = (By.CSS_SELECTOR, 'div.item-country')
    NUMBER_INPUT = (By.CSS_SELECTOR, '#mat-input-0')
    TERMS = (By.CSS_SELECTOR, '.custom-checkbox')
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'button.btn-continue')
    CODE_INPUT = (By.CSS_SELECTOR, 'input#code6')
    
    """HEADER"""
    DOCTOR_NAME = (By.CSS_SELECTOR, 'div.doctor-name')
    BUTTON_BEGIN_WORK_DAY = (By.CSS_SELECTOR, 'button.btn-start')
    EXIT_ERROR = (By.CSS_SELECTOR, '#toast-container div')
    OPEN_PROFILE_LIST = (By.CSS_SELECTOR, 'div.doctor')
    BUTTON_LOGOUT = (By.CSS_SELECTOR, 'a.link-logout')
    LOGOUT_ERROR = (By.CSS_SELECTOR, '#toast-container div')

    # Checking video/audio
    VIDEO_YES = (By.CSS_SELECTOR, '.slide-video-check button.btn-border:nth-child(2)')
    VIDEO_NO = (By.CSS_SELECTOR, '.slide-video-check button.btn-border:nth-child(1)')
    BUTTON_BEGIN_RECORD = (By.CSS_SELECTOR, 'button.btn-start-record')
    BUTTON_STOP_RECORD = (By.CSS_SELECTOR, 'button.btn-stop-record')
    BUTTON_PLAY_RECORD = (By.CSS_SELECTOR, 'button.btn-play-record')
    AUDIO_YES = (By.CSS_SELECTOR, 'div.slide-footer.ng-star-inserted .btn-border:nth-child(2)')
    AUDIO_NO = (By.CSS_SELECTOR, 'div.slide-footer.ng-star-inserted .btn-border:nth-child(1)')
    VIDEO_STATUS = (By.CSS_SELECTOR, '.modal-body li.chanel-video.offline')
    CLOSE_POPUP_CHANNELS = (By.CSS_SELECTOR, 'app-devices-checking button.btn-start')

    """REQUESTS"""
    LIST_ALL_REQUESTS = (By.CSS_SELECTOR, 'app-appointment-item')
    CURRENT_REQUEST_NAME = (By.CSS_SELECTOR, '.active-background .diagnose-name')
    # Progress bar
    PROGRESS_SYMPTOME = (By.CSS_SELECTOR, '.active-background .progress-icon-list')
    PROGRESS_CONCLUSION = (By.CSS_SELECTOR, '.active-background .progress-icon-union')
    PROGRESS_ANALYSIS = (By.CSS_SELECTOR, '.active-background .progress-icon-vector')
    PROGRESS_DRUG = (By.CSS_SELECTOR, '.active-background .progress-icon-tablet')

    """REQUEST INFO"""
    # Symptomes
    SEARCH_SYMPTOM = (By.CSS_SELECTOR, '.wrapper-symptoms input')
    RESULT_SEARCH_SYMPTOM = (By.CSS_SELECTOR, 'div.ng-option-marked')
    LIST_ALL_SYMPTOMED = (By.CSS_SELECTOR, 'div.symptom-item')
    DELETE_SYMPTOM = (By.CSS_SELECTOR, 'div.delete-symptom')
    # Conclusions
    LIST_ALL_CONCLUSIONS = (By.CSS_SELECTOR, 'div.conclusion-item')
    LIST_ALL_NO_ACTIVE_CONCLUSIONS = (By.CSS_SELECTOR, 'div.bg-no-active')
    APPROVE_CONCLUSION = (By.CSS_SELECTOR, 'div.conclusion-icon')
    SEARCH_CONCLUSION = (By.CSS_SELECTOR, '.consultation-wrapper input')
    RESULT_SEARCH_CONCLUSION = (By.CSS_SELECTOR, 'div.ng-option-marked')
    DELETE_CONCLUSION = (By.CSS_SELECTOR, 'div.icon-delete')
    # Analysis
    SEARCH_ANALYSIS = (By.CSS_SELECTOR, '.wrapper-find-analysis input')
    RESULT_SEARCH_ANALYSIS = (By.CSS_SELECTOR, '.ng-option-marked')
    # Drugs
    SEARCH_DRUG = (By.CSS_SELECTOR, 'div.find-prescriptions input')
    RESULT_SEARCH_DRUG = (By.CSS_SELECTOR, '.ng-option-marked')
    # Save appointment
    BUTTON_SAVE = (By.CSS_SELECTOR, 'button.save-appointment')
    
    """========== GENERAL =========="""

    @allure.step('Авторизация пользователя "{number}" / страна "{country}"')
    def login(self, number, country):
        """
        Авторизация пользователя
        """
        self.send_keys(self.NUMBER_INPUT, value=number)
        self.click(self.TERMS)
        self.click(self.LOGIN_BUTTON)
        self.send_keys(self.CODE_INPUT, value=Keys.ENTER)
        return self.get_element(self.DOCTOR_NAME).text 

    @allure.step('Начало рабочего дня и проверка гарнитуры. Видео: "{is_video}" Аудио: "{is_audio}"')
    def start_work_day(self, is_video, is_audio):
        """
        Начинает рабочий день и проходит проверку гарнитуры.
        """
        self.click(self.BUTTON_BEGIN_WORK_DAY)
        # разрешение на микр игнорируется
        self.click(self.BUTTON_BEGIN_RECORD)
        self.click(self.BUTTON_STOP_RECORD)
        self.click(self.BUTTON_PLAY_RECORD)
        if is_audio:
            self.click(self.AUDIO_YES)
            if is_video:
                # разрешение видео игнорируется
                self.click(self.VIDEO_YES)
            else:
                self.click(self.VIDEO_NO)
        else:
            self.click(self.AUDIO_NO)

    @allure.step('Выделяется заявка номер: "{number}"')
    def select_request(self, number):
        """
        Выделяет заявку в списке по {number}.
        """
        self.get_elements(self.LIST_ALL_REQUESTS)[number].click()

    @allure.step("Выход из аккаунта")
    def logout(self):
        self.click(self.OPEN_PROFILE_LIST)
        self.click(self.BUTTON_LOGOUT)

    """========== APPOINTMENT INFO =========="""

    @allure.step('Поиск и добавление симптома: "{symptom}"')
    def add_symptom(self, symptom):
        """
        Ищет симптом по тексту и добавляет его из результата поиска в обращение.
        """
        self.send_keys(self.SEARCH_SYMPTOM, value=symptom)
        self.click(self.RESULT_SEARCH_SYMPTOM)

    @allure.step('Удаление симптома: "{symptom}"')
    def delete_symptom(self, symptom):
        """
        Удаляет симптом из обращения по тексту.
        """
        list_symptomes = self.get_elements(self.LIST_ALL_SYMPTOMED)
        for each in list_symptomes:
            if symptom in each.text:
                each.click()
        self.click(self.DELETE_SYMPTOM)

    @allure.step('Удаление подтвержденного диагноза в текущем выделеном обращении')
    def clear_conclusions(self):
        self.click(self.DELETE_CONCLUSION)

    @allure.step('Поиск, добавление и подтверждение диагноза: "{conclusion}"')
    def add_conclusion(self, conclusion):
        if not self.is_exist(self.LIST_ALL_CONCLUSIONS):
                # way 1 if need search conclusion
            self.send_keys(self.SEARCH_CONCLUSION, value=conclusion)
            self.click(self.RESULT_SEARCH_CONCLUSION)
            self.click(self.APPROVE_CONCLUSION)
            return True

        all_conclusions = self.get_elements(self.LIST_ALL_CONCLUSIONS)
        i = 0
        for each in all_conclusions:
            # way 2 select from suggest
            if conclusion in each.text.split(' ')[0].split('\n')[0]:
                self.get_elements(self.APPROVE_CONCLUSION)[i].click()
                break
            i += 1

    @allure.step('Поиск и добавления анализа: "{analysis}"')
    def add_analysis(self, analysis):
        self.send_keys(self.SEARCH_ANALYSIS, value=analysis)
        self.click(self.RESULT_SEARCH_ANALYSIS)

    @allure.step('Поиск и добавление препарата: "{drug}"')
    def add_drug(self, drug):
        self.send_keys(self.SEARCH_DRUG, value=drug)
        self.click(self.RESULT_SEARCH_DRUG)
    

    @allure.step('Клик на кнопку "Завершить назначение"')
    def save_appointment(self):
        self.click(self.BUTTON_SAVE)

    """========== VERIFY =========="""

    @allure.step('Проверка что первый диагноз в списке диагнозов соответствует диагнозу: "{conclusion}"')
    def verify_first_conclusion_is(self, conclusion):
        if self.get_conclusion_position(conclusion) == 1:
        # if conclusion in self.get_elements(self.LIST_ALL_CONCLUSIONS)[0].text.split(' ')[0].split('\n')[0]:
            self.click(self.DELETE_CONCLUSION)
            return True
        else:
            self.click(self.DELETE_CONCLUSION)
            return False

    @allure.step('Получение позиции текущего выделеного обращения в списке обращений')
    def get_conclusion_position(self, conclusion):
        """
        Возвращает int позицию в обращениях текущего выделенного обращения
        """
        list_conclusions = self.get_elements(self.LIST_ALL_CONCLUSIONS)
        i = 1
        for each in list_conclusions:
            if conclusion in each.text.split(' ')[0].split('n')[0]:
                return i
            i += 1

    @allure.step('Деактивация назначенного диагноза в текущем выделенном обращении')
    def deactivate_conclusion(self):
        self.click(self.DELETE_CONCLUSION)

    @allure.step('Проверка блокировки других диагнозов')
    def verify_block_conclusions(self):
        """"return True if blocked conclusions -1 of all conclusions"""
        if self.is_exist(self.DELETE_CONCLUSION):
            if (len(self.get_elements(self.LIST_ALL_CONCLUSIONS)) - 1) == len(self.get_elements(self.LIST_ALL_NO_ACTIVE_CONCLUSIONS)):
                self.click(self.DELETE_CONCLUSION)
                return True
            else:
                self.click(self.DELETE_CONCLUSION)
                return False
        else:
            return False

    @allure.step('Проверка отображения ошибки при выходе')
    def is_present_logout_error(self):
        # need add close error msg
        return self.is_exist(self.LOGOUT_ERROR)

    @allure.step('Проверка отображения ошибки при завершении обращения')
    def is_present_save_error(self):
        # need add close error msg
        return self.is_exist(self.EXIT_ERROR)

    @allure.step('Получить заголовок обращения в панели обращений текущего выделенного обращения')
    def current_request_name(self):
        return self.get_element(self.CURRENT_REQUEST_NAME).text

    @allure.step('Проверка активности иконки прогресса Симптомов"')
    def is_indicator_symptomes(self):
        return self.is_exist(self.PROGRESS_SYMPTOME)

    @allure.step('Проверка активности иконки прогресса Диагнозов')
    def is_indicator_diagnosis(self):
        return self.is_exist(self.PROGRESS_CONCLUSION)

    @allure.step('Проверка активности иконки прогресса Анализов')
    def is_indicator_analysis(self):
        return self.is_exist(self.PROGRESS_ANALYSIS)

    @allure.step('Проверка активности иконки прогресса Препаратов')
    def is_indicator_drug(self):
        return self.is_exist(self.PROGRESS_DRUG)

    @allure.step('Проверка отображения предлогаемых диагнозов')
    def verify_no_conclusion(self):
        """
        Возвращает True если в обращении нет предложенных диагнозов.
        """
        is_diagnosis_displayed = self.is_exist(self.LIST_ALL_CONCLUSIONS)
        return not is_diagnosis_displayed

    @allure.step('Проверка состояния видео канала')
    def verify_video_active(self):
        """
        Возвращает True если видео канал доступен и False если не доступен. (Проверка в попапе.)
        """
        is_video_active = self.is_exist(self.VIDEO_STATUS)
        logging.info(is_video_active)
        self.click(self.CLOSE_POPUP_CHANNELS)
        return is_video_active
