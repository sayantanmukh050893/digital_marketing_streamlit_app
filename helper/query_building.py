import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math
from functools import reduce

def simpify_ratio(a,b,c):
    gcd_all = reduce(math.gcd, [a,b,c])
    return (a//gcd_all, b//gcd_all, c//gcd_all)

def create_query(vertical, campaign_type, month, year, overall_performance, summary):
    """
    Create a query based on the selected brand, month, year, and uploaded Excel file.
    """
    # Read the Excel file into a DataFrame

    query_text = "For a specific company in " + vertical + " sector the performance and ad-spend for a particular month is as follows : \n\n"

    #overall_performance = pd.read_excel(excel_file, sheet_name="overall_performance")
    #overall_performance = overall_performance[overall_performance["brand"] == brand]
    overall_performance = overall_performance[overall_performance["month"] == month]
    overall_performance = overall_performance[overall_performance["year"] == int(year)]  

    overall_ctr = overall_performance["ctr"].values[0]
    overall_conv_rate = overall_performance["conv_rate"].values[0]
    overall_roas = overall_performance["roas"].values[0]

    query_text += "Performance :\n\nOverall ctr : " + str(overall_ctr) + " %" + "\nOverall conversion rate : " + str(overall_conv_rate) + " %" + "\nOverall roas : " + str(overall_roas) + "\n\n"

    #summary = pd.read_excel(excel_file, sheet_name="summary")
    summary = summary[(summary["month"] == month) & (summary["year"] == int(year))]
    #summary = summary[(summary["brand"] == brand) & (summary["month"] == month) & (summary["year"] == int(year))]

    total_budget = summary["media_cost"].sum()
    video_budget = summary[summary["type"]=="digital"]["media_cost"].sum()
    banner_budget = summary[summary["type"]=="banner"]["media_cost"].sum()
    video_budget_percentage = np.round((video_budget / total_budget) * 100,2)
    banner_budget_percentage = np.round((banner_budget / total_budget) * 100,2)

    query_text += "Advertising Strategy :\n\nVideo Budget : " + str(video_budget_percentage) +"%"+ "\nBanner Budget : " + str(banner_budget_percentage) + "%\n\n"

    query_text += "The percentage of CTR and Media Cost for different channels of video marketing are as follows :\n\nDemand-Side Platform : \n\n"

    summary_dsp_digital = summary[(summary["type"]=="digital") & (summary["platform"]=="demand-side")]
    summary_dsp_digital_media_cost_total = summary_dsp_digital["media_cost"].sum()
    for name,ctr_perc,media_cost in zip(summary_dsp_digital["ad_name"],summary_dsp_digital["estimated_ctr"],summary_dsp_digital["media_cost"]):
        media_cost_perc = np.round(media_cost/summary_dsp_digital_media_cost_total*100,2)
        query_text += name + " : " + str(ctr_perc) + " %" + " - " + str(media_cost_perc) + "%\n"
    
    
    query_text+= "\nBiddable Platform : \n\n"
    summary_biddable_digital = summary[(summary["type"]=="digital") & (summary["platform"]=="biddable")]
    summary_biddable_digital_media_cost_total = summary_biddable_digital["media_cost"].sum()
    for name,ctr_perc,media_cost in zip(summary_biddable_digital["ad_name"],summary_biddable_digital["estimated_ctr"],summary_biddable_digital["media_cost"]):
        media_cost_perc = np.round(media_cost/summary_biddable_digital_media_cost_total*100,2)
        query_text += name + " : " + str(ctr_perc) + " %" + " - " + str(media_cost_perc) + "%\n"

    query_text+= "\nSocial Platform : \n\n"
    summary_social_digital = summary[(summary["type"]=="digital") & (summary["platform"]=="social")]
    summary_social_digital_media_cost_total = summary_social_digital["media_cost"].sum()
    for name,ctr_perc,media_cost in zip(summary_social_digital["ad_name"],summary_social_digital["estimated_ctr"],summary_social_digital["media_cost"]):
        media_cost_perc = np.round(media_cost/summary_social_digital_media_cost_total*100,2)
        query_text += name + " : " + str(ctr_perc) + " %" + " - " + str(media_cost_perc) + "%\n"
    
    ratio = simpify_ratio(summary_dsp_digital_media_cost_total,summary_biddable_digital_media_cost_total,summary_social_digital_media_cost_total)
    query_text += "\nThe ratio of overall ad-spend for the demand-side, biddable, social platforms is : " + str(ratio[0]) + ":" + str(ratio[1]) + ":" + str(ratio[2]) + "\n\n"
    
    query_text += "\nThe percentage of CTR and Media Cost for different channels of banner marketing are as follows :\n"
    summary_banner = summary[summary["type"]=="banner"]
    summary_banner_media_cost_total = summary_banner["media_cost"].sum()
    for name,ctr_perc,media_cost in zip(summary_banner["ad_name"],summary_banner["estimated_ctr"],summary_banner["media_cost"]):
        media_cost_perc = np.round(media_cost/summary_banner_media_cost_total*100,2)
        query_text += name + " : " + str(ctr_perc) + " %" + " - " + str(media_cost_perc) + "%\n"
    
    query_text += "\nWhat should be the " +campaign_type+ " based advertising strategy of that company at different platform and in video and banner level in the upcoming month so as to increase the overall performance in terms on ctr, Conv Rate and ROAS ? "


    return query_text