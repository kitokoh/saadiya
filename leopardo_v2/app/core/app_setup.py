"""
This module contains the setup functions for the Leopardo V2 application.
"""

from ..features.home import create_home_feature
from ..features.marketing import create_marketing_feature
from ..features.sales import create_sales_feature
from ..features.run import create_run_feature
from ..features.finance import create_finance_feature
from ..features.settings import create_settings_feature
from ..features.tools import create_tools_feature
from ..features.telecommande import create_telecommande_feature
from ..features.instances import create_instances_feature
from ..features.premierepage import create_premierepage_feature
from ..features.statistics import create_statistics_feature
from ..features.facebook import create_facebook_feature
from ..features.instagram import create_instagram_feature
from ..features.linkedin import create_linkedin_feature
from ..features.twitter import create_twitter_feature
from ..features.youtube import create_youtube_feature
from ..features.pinterest import create_pinterest_feature
from ..features.reddit import create_reddit_feature
from ..features.snapchat import create_snapchat_feature
from ..features.tiktok import create_tiktok_feature
from ..features.whasapping import create_whasapping_feature
from ..features.autoblog import create_autoblog_feature
from ..features.adspro import create_adspro_feature
from ..features.branding import create_branding_feature
from ..features.chatbot import create_chatbot_feature
from ..features.placeholders import PlaceholderWidget
from .decorators import pro_feature

def init_features(main_window):
    """
    Initializes the features of the application.

    Args:
        main_window: The main window of the application.
    """
    main_window.home_widget, main_window.home_controller = create_home_feature()
    main_window.marketing_widget, main_window.marketing_controller = create_marketing_feature()
    main_window.sales_widget, main_window.sales_controller = create_sales_feature()
    main_window.run_widget, main_window.run_controller = create_run_feature()
    main_window.finance_widget, main_window.finance_controller = create_finance_feature()
    main_window.settings_widget, main_window.settings_controller = create_settings_feature()
    main_window.tools_widget, main_window.tools_controller = create_tools_feature()
    main_window.telecommande_widget, main_window.telecommande_controller = create_telecommande_feature()
    main_window.instances_widget, main_window.instances_controller = create_instances_feature()
    main_window.premierepage_widget, main_window.premierepage_controller = create_premierepage_feature()
    main_window.statistics_widget, main_window.statistics_controller = create_statistics_feature()
    main_window.facebook_widget, main_window.facebook_controller = create_facebook_feature()
    main_window.facebook_widget.set_controller(main_window.facebook_controller)
    main_window.instagram_widget, main_window.instagram_controller = create_instagram_feature()
    main_window.instagram_widget.set_controller(main_window.instagram_controller)
    main_window.linkedin_widget, main_window.linkedin_controller = create_linkedin_feature()
    main_window.linkedin_widget.set_controller(main_window.linkedin_controller)
    main_window.twitter_widget, main_window.twitter_controller = create_twitter_feature()
    main_window.twitter_widget.set_controller(main_window.twitter_controller)
    main_window.youtube_widget, main_window.youtube_controller = create_youtube_feature()
    main_window.pinterest_widget, main_window.pinterest_controller = create_pinterest_feature()
    main_window.reddit_widget, main_window.reddit_controller = create_reddit_feature()
    main_window.snapchat_widget, main_window.snapchat_controller = create_snapchat_feature()
    main_window.tiktok_widget, main_window.tiktok_controller = create_tiktok_feature()
    main_window.whasapping_widget, main_window.whasapping_controller = create_whasapping_feature()
    main_window.autoblog_widget, main_window.autoblog_controller = create_autoblog_feature()
    main_window.adspro_widget, main_window.adspro_controller = create_adspro_feature()
    main_window.branding_widget, main_window.branding_controller = create_branding_feature()
    main_window.chatbot_widget, main_window.chatbot_controller = create_chatbot_feature()

    # Placeholders for new features
    main_window.my_media_widget = PlaceholderWidget("My Media")
    main_window.my_groups_widget = PlaceholderWidget("My Groups")
    main_window.marketing_robots_widget = PlaceholderWidget("Marketing Robots")
    main_window.ads_manager_widget = PlaceholderWidget("Ads Manager")
    main_window.campaign_scheduler_widget = PlaceholderWidget("Campaign Scheduler")
    main_window.email_sms_widget = PlaceholderWidget("Email & SMS")
    main_window.content_generator_widget = PlaceholderWidget("Content Generator")
    main_window.project_management_widget = PlaceholderWidget("Project Management")
    main_window.sav_widget = PlaceholderWidget("SAV")
    main_window.short_links_trackers_widget = PlaceholderWidget("Short Links & Trackers")
    main_window.prospection_relances_widget = PlaceholderWidget("Prospection & Relances")
    main_window.dms_quotes_widget = PlaceholderWidget("DMS & Quotes")
    main_window.crm_widget = PlaceholderWidget("CRM")
    main_window.sales_prompts_templates_widget = PlaceholderWidget("Sales Prompts / Templates")
    main_window.auto_responder_widget = PlaceholderWidget("Auto-Responder")
    main_window.sales_assistant_widget = PlaceholderWidget("Sales Assistant")
    main_window.prompts_tools_widget = PlaceholderWidget("Prompts & Tools")
    main_window.competitor_analysis_widget = PlaceholderWidget("Competitor Analysis")
    main_window.assistant_ventes_widget = PlaceholderWidget("Assistant ventes")
    main_window.ai_workflows_widget = PlaceholderWidget("AI Workflows")
    main_window.invoices_billing_widget = PlaceholderWidget("Invoices & Billing")
    main_window.trader_widget = PlaceholderWidget("Trader")

    # Add widgets to the content stack
    main_window.content_stack.addWidget(main_window.premierepage_widget)
    main_window.content_stack.addWidget(main_window.home_widget)
    main_window.content_stack.addWidget(main_window.marketing_widget)
    main_window.content_stack.addWidget(main_window.sales_widget)
    main_window.content_stack.addWidget(main_window.run_widget)
    main_window.content_stack.addWidget(main_window.finance_widget)
    main_window.content_stack.addWidget(main_window.settings_widget)
    main_window.content_stack.addWidget(main_window.tools_widget)
    main_window.content_stack.addWidget(main_window.telecommande_widget)
    main_window.content_stack.addWidget(main_window.instances_widget)
    main_window.content_stack.addWidget(main_window.statistics_widget)
    main_window.content_stack.addWidget(main_window.facebook_widget)
    main_window.content_stack.addWidget(main_window.instagram_widget)
    main_window.content_stack.addWidget(main_window.linkedin_widget)
    main_window.content_stack.addWidget(main_window.twitter_widget)
    main_window.content_stack.addWidget(main_window.youtube_widget)
    main_window.content_stack.addWidget(main_window.pinterest_widget)
    main_window.content_stack.addWidget(main_window.reddit_widget)
    main_window.content_stack.addWidget(main_window.snapchat_widget)
    main_window.content_stack.addWidget(main_window.tiktok_widget)
    main_window.content_stack.addWidget(main_window.whasapping_widget)
    main_window.content_stack.addWidget(main_window.autoblog_widget)
    main_window.content_stack.addWidget(main_window.adspro_widget)
    main_window.content_stack.addWidget(main_window.branding_widget)
    main_window.content_stack.addWidget(main_window.chatbot_widget)
    main_window.content_stack.addWidget(main_window.my_media_widget)
    main_window.content_stack.addWidget(main_window.my_groups_widget)
    main_window.content_stack.addWidget(main_window.marketing_robots_widget)
    main_window.content_stack.addWidget(main_window.ads_manager_widget)
    main_window.content_stack.addWidget(main_window.campaign_scheduler_widget)
    main_window.content_stack.addWidget(main_window.email_sms_widget)
    main_window.content_stack.addWidget(main_window.content_generator_widget)
    main_window.content_stack.addWidget(main_window.project_management_widget)
    main_window.content_stack.addWidget(main_window.sav_widget)
    main_window.content_stack.addWidget(main_window.short_links_trackers_widget)
    main_window.content_stack.addWidget(main_window.prospection_relances_widget)
    main_window.content_stack.addWidget(main_window.dms_quotes_widget)
    main_window.content_stack.addWidget(main_window.crm_widget)
    main_window.content_stack.addWidget(main_window.sales_prompts_templates_widget)
    main_window.content_stack.addWidget(main_window.auto_responder_widget)
    main_window.content_stack.addWidget(main_window.sales_assistant_widget)
    main_window.content_stack.addWidget(main_window.prompts_tools_widget)
    main_window.content_stack.addWidget(main_window.competitor_analysis_widget)
    main_window.content_stack.addWidget(main_window.assistant_ventes_widget)
    main_window.content_stack.addWidget(main_window.ai_workflows_widget)
    main_window.content_stack.addWidget(main_window.invoices_billing_widget)
    main_window.content_stack.addWidget(main_window.trader_widget)

    main_window.content_stack.setCurrentWidget(main_window.premierepage_widget)

def connect_signals(main_window):
    """
    Connects the signals of the application.

    Args:
        main_window: The main window of the application.
    """
    # Main menu
    main_window.side_menu.home_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.home_widget))
    main_window.side_menu.marketing_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.marketing_widget))
    main_window.side_menu.sales_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.sales_widget))
    main_window.side_menu.run_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.run_widget))
    main_window.side_menu.anciens_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.tools_widget))
    main_window.side_menu.telecommande_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.telecommande_widget))
    main_window.side_menu.instances_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.instances_widget))
    main_window.side_menu.statistics_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.statistics_widget))
    main_window.side_menu.facebook_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.facebook_widget))
    main_window.side_menu.instagram_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.instagram_widget))
    main_window.side_menu.linkedin_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.linkedin_widget))
    main_window.side_menu.twitter_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.twitter_widget))
    main_window.side_menu.youtube_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.youtube_widget))
    main_window.side_menu.pinterest_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.pinterest_widget))
    main_window.side_menu.reddit_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.reddit_widget))
    main_window.side_menu.snapchat_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.snapchat_widget))
    main_window.side_menu.tiktok_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.tiktok_widget))
    main_window.side_menu.whasapping_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.whasapping_widget))
    main_window.side_menu.autoblog_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.autoblog_widget))
    main_window.side_menu.adspro_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.adspro_widget))
    main_window.side_menu.branding_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.branding_widget))
    main_window.side_menu.chatbot_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.chatbot_widget))

    # Pro features
    connect_pro_features(main_window)

    # Marketing Menu
    main_window.side_menu.marketing_menu.actions()[0].triggered.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.my_media_widget))
    main_window.side_menu.marketing_menu.actions()[1].triggered.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.my_groups_widget))
    main_window.side_menu.marketing_menu.actions()[2].triggered.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.marketing_robots_widget))
    main_window.side_menu.marketing_menu.actions()[3].triggered.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.ads_manager_widget))
    main_window.side_menu.marketing_menu.actions()[4].triggered.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.campaign_scheduler_widget))
    main_window.side_menu.marketing_menu.actions()[5].triggered.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.email_sms_widget))
    main_window.side_menu.marketing_menu.actions()[6].triggered.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.content_generator_widget))

    # Sales Menu
    main_window.side_menu.sales_menu.actions()[0].triggered.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.project_management_widget))
    main_window.side_menu.sales_menu.actions()[1].triggered.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.sav_widget))
    main_window.side_menu.sales_menu.actions()[2].triggered.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.short_links_trackers_widget))
    main_window.side_menu.sales_menu.actions()[3].triggered.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.prospection_relances_widget))
    main_window.side_menu.sales_menu.actions()[4].triggered.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.dms_quotes_widget))
    main_window.side_menu.sales_menu.actions()[5].triggered.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.crm_widget))
    main_window.side_menu.sales_menu.actions()[6].triggered.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.sales_prompts_templates_widget))

    # Language switching
    main_window.side_menu.language_menu.actions()[0].triggered.connect(lambda: main_window.language_manager.switch_language('en'))
    main_window.side_menu.language_menu.actions()[1].triggered.connect(lambda: main_window.language_manager.switch_language('fr'))
    main_window.side_menu.language_menu.actions()[2].triggered.connect(lambda: main_window.language_manager.switch_language('tr'))
    main_window.side_menu.language_menu.actions()[3].triggered.connect(lambda: main_window.language_manager.switch_language('ar'))
    main_window.side_menu.language_menu.actions()[4].triggered.connect(lambda: main_window.language_manager.switch_language('pt'))

    # User Profile
    main_window.side_menu.user_profile.login_button.clicked.connect(main_window.show_login_dialog)
    main_window.side_menu.user_profile.logout_button.clicked.connect(main_window.logout)
    main_window.side_menu.user_profile.enterprise_button.clicked.connect(main_window.switch_to_enterprise)
    main_window.side_menu.user_profile.personal_button.clicked.connect(main_window.switch_to_personal)

    # Menu Config
    main_window.side_menu.menu_config_button.clicked.connect(main_window.show_menu_config_dialog)

    # Top menu actions
    main_window.top_menu.file_menu.addAction("Show Notification").triggered.connect(lambda: main_window.notification_service.show_notification("Test", "This is a test notification."))
    main_window.top_menu.file_menu.addAction("Check for Updates").triggered.connect(main_window.updater_service.check_for_updates)

@pro_feature("pro")
def connect_pro_features(main_window):
    """
    Connects the signals of the pro features.

    Args:
        main_window: The main window of the application.
    """
    main_window.side_menu.ai_agent_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.prompts_tools_widget))
    main_window.side_menu.finance_button.clicked.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.finance_widget))
    main_window.side_menu.upgrade_button.clicked.connect(main_window.show_upgrade_window)

    # AI Agent Menu
    main_window.side_menu.ai_agent_menu.actions()[0].triggered.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.auto_responder_widget))
    main_window.side_menu.ai_agent_menu.actions()[1].triggered.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.sales_assistant_widget))
    main_window.side_menu.ai_agent_menu.actions()[2].triggered.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.prompts_tools_widget))
    main_window.side_menu.ai_agent_menu.actions()[3].triggered.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.competitor_analysis_widget))
    main_window.side_menu.ai_agent_menu.actions()[4].triggered.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.assistant_ventes_widget))
    main_window.side_menu.ai_agent_menu.actions()[5].triggered.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.ai_workflows_widget))

    # Finance Menu
    main_window.side_menu.finance_menu.actions()[0].triggered.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.invoices_billing_widget))
    main_window.side_menu.finance_menu.actions()[1].triggered.connect(lambda: main_window.content_stack.setCurrentWidget(main_window.trader_widget))
