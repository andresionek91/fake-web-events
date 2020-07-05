from faker import Faker
import json
from fake_web_events import select_random
import uuid
import random


class User(Faker):
    """
    Class that will create fake event attributes associated to a user
    """

    def __init__(self):
        super().__init__(['en_US'])
        self.lat, self.lng, self.region, self.country, self.timezone = self.location_on_land()
        self.os_name = select_random('operating_systems')
        self.browser_name = select_random('browsers')
        self.device_is_mobile = False
        self.device_type = 'Computer'
        self.ad = select_random('ads')
        self.campaign = select_random('campaigns')
        self.marketing_medium = select_random('marketing_mediums')
        self.referer_name = select_random('marketing_sources')
        self.referer_medium = 'search' if self.referer_name in ['google', 'bing'] else 'internal'
        self.referer_url = f'www.{self.referer_name}.com'

    def geo(self):
        """
        Build dictionary with geo attributes
        """
        return dict(
            geo_latitude=self.lat,
            geo_longitude=self.lng,
            geo_country=self.country,
            geo_timezone=self.timezone,
            geo_region_name=self.region
        )

    def ip(self):
        """
        Build dictionary with ip attributes
        """
        return dict(
            ip_address=self.ipv4_public(),
        )

    def browser(self):
        """
        Build dictionary with browser attributes
        """
        user_agents_dict = {
            'Chrome': self.chrome(),
            'InternetExplorer': self.internet_explorer(),
            'Firefox': self.firefox(),
            'Safari': self.safari(),
            'Opera': self.opera()
         }
        return dict(
            browser_name=self.browser_name,
            browser_user_agent=user_agents_dict[self.browser_name],
            browser_language=self.locale(),
        )

    def operating_system(self):
        """
        Build dictionary with operating_system attributes
        """
        os_dict = {
            'Windows': self.windows_platform_token(),
            'MacOS': self.mac_platform_token(),
            'Linux': self.linux_platform_token(),
            'Android': self.android_platform_token(),
            'iOS': self.ios_platform_token()
         }

        return dict(
            os=os_dict[self.os_name],
            os_name=self.os_name,
            os_timezone=self.timezone
        )

    def device(self):
        """
        Build dictionary with device type attributes
        """
        if self.os_name in ['Android', 'iOS']:
            self.device_type = 'Mobile'
            self.device_is_mobile = True

        return dict(
            device_type=self.device_type,
            device_is_mobile=self.device_is_mobile
        )

    def user(self):
        """
        Build dictionary with user attributes
        """
        return dict(
            user_custom_id=self.ascii_free_email(),
            user_domain_id=str(uuid.uuid4())
        )

    def referer(self):
        """
        Build dictionary with referer type attributes
        """
        return dict(
            referer_url=self.referer_url,
            referer_url_scheme='http',
            referer_url_port='80',
            referer_medium=self.referer_medium,
        )

    def marketing(self):
        """
        Build dictionary with marketing attributes
        """
        return dict(
            marketing_medium=self.marketing_medium,
            marketing_source=self.referer_name,
            marketing_content=self.ad,
            marketing_campaign=self.campaign,
            marketing_click_id=str(uuid.uuid4()),
            )

    def asdict(self):
        """
        Return dict with all user attributes
        """
        return {
            **self.referer(),
            **self.marketing(),
            **self.geo(),
            **self.ip(),
            **self.browser(),
            **self.operating_system(),
            **self.device(),
            **self.user()
        }

    def __str__(self):
        """
        Human readable attributes
        """
        return json.dumps(self.asdict(), indent=4, ensure_ascii=False)


class UserPool:

    def __init__(self, size):
        self.pool = [User()] * size

    def __repr__(self):
        return repr(self.pool)

    def get_user(self):
        """
        Get a random user with reposition
        """
        return random.choices(self.pool)[0]
