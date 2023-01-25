import os
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestFight():
    def setup_method(self, method):
        self.event_ep = os.environ.get('EVENT_EP')
        self.fight_ep = os.environ.get('FIGHT_EP')

        options = webdriver.FirefoxOptions()
        # options = webdriver.EdgeOptions()
        # options = webdriver.ChromeOptions()

        options.set_capability("se:recordVideo", True)
        options.set_capability("se:timeZone", "Australia/ACT")
        options.set_capability("se:screenResolution", "1280x1280")

        command_executor = os.environ.get('SEL_EP')

        self.driver = webdriver.Remote(command_executor=command_executor,
                                       options=options)
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_fight(self):
        # Check the current number of battles in event-statistics
        self.driver.get(self.event_ep)
        time.sleep(2)
        num_battle_before = int(self.driver.find_element(By.ID, "numBattles").text.split()[0])
        logging.getLogger().info("Initial number of battles: %d", num_battle_before)

        # Pick a new set of fighter and run a fight
        self.driver.get(self.fight_ep)
        for i in range(1, 3):
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, ".btn-primary > h4").click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-danger > h4").click()
        self.driver.execute_script("window.scrollTo(0, 1920)")
        time.sleep(1)

        # Check the updated number of battles in event-statistic
        self.driver.get(self.event_ep)
        time.sleep(3)
        num_battle_after = int(self.driver.find_element(By.ID, "numBattles").text.split()[0])
        logging.getLogger().info("Updated number of battles: %d", num_battle_after)

        # the updated number of battle should be equal to the previous number of battler, plus 1.
        assert num_battle_before + 1 == num_battle_after
