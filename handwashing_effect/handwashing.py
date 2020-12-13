# importing modules
import pandas as pd
# Read datasets/yearly_deaths_by_clinic.csv into yearly
yearly = pd.read_csv("datasets/yearly_deaths_by_clinic.csv")

# Print out yearly
yearly

# Calculate proportion of deaths per no. births
yearly["proportion_deaths"] = yearly["deaths"]/yearly["births"]
# Extract clinic 1 data into yearly1 and clinic 2 data into yearly2
yearly1 = yearly[yearly["clinic"]=="clinic 1"]
yearly2 = yearly[yearly["clinic"]=="clinic 2"]

# Print out yearly1

yearly1

# This makes plots appear in the notebook
get_ipython().run_line_magic('matplotlib', 'inline')

# Plot yearly proportion of deaths at the two clinics
ax=yearly1.plot(x="year",y="proportion_deaths",label="clinic 1")
yearly2.plot(x="year",y="proportion_deaths",label="clinic 2",ax=ax)
ax.set_ylabel("proportion_death")

# Read datasets/monthly_deaths.csv into monthly
monthly = pd.read_csv("datasets/monthly_deaths.csv",parse_dates=["date"])
# Calculate proportion of deaths per no. births
monthly["proportion_deaths"] = monthly["deaths"]/monthly["births"]
# Print out the first rows in monthly
monthly.head()

# Plot monthly proportion of deaths

get_ipython().run_line_magic('matplotlib', 'inline')
ax=monthly.plot(x="date",y="proportion_deaths")
ax.set_ylabel("proportion_deaths")


# In[30]:


get_ipython().run_cell_magic('nose', '', '        \ndef test_ax_exists():\n    assert \'ax\' in globals(), \\\n        "The result of the plot method should be assigned to a variable called ax"\n\ndef test_plot_plots_correct_data():\n    y0 = ax.get_lines()[0].get_ydata()\n    assert all(monthly["proportion_deaths"] == y0), \\\n        "The plot should show the column \'proportion_deaths\' in monthly."')


# ## 6. The effect of handwashing highlighted
# <p>Starting from the summer of 1847 the proportion of deaths is drastically reduced and, yes, this was when Semmelweis made handwashing obligatory. </p>
# <p>The effect of handwashing is made even more clear if we highlight this in the graph.</p>

# Date when handwashing was made mandatory
import pandas as pd
handwashing_start = pd.to_datetime('1847-06-01')

# Split monthly into before and after handwashing_start
before_washing = monthly[monthly["date"] < handwashing_start]
after_washing = monthly[monthly["date"] >= handwashing_start]

# Plot monthly proportion of deaths before and after handwashing
ax = before_washing.plot(x="date", y="proportion_deaths",
                         label="Before handwashing")
after_washing.plot(x="date", y="proportion_deaths",
                   label="After handwashing", ax=ax)
ax.set_ylabel("Proportion deaths")


# In[32]:


get_ipython().run_cell_magic('nose', '', '\ndef test_before_washing_correct():\n    correct_before_washing = monthly[monthly["date"] < handwashing_start]\n    try:\n        pd.testing.assert_frame_equal(before_washing, correct_before_washing)\n    except AssertionError:\n        assert False, "before_washing should contain the rows of monthly < handwashing_start" \n\ndef test_after_washing_correct():\n    correct_after_washing = monthly[monthly["date"] >= handwashing_start]\n    try:\n        pd.testing.assert_frame_equal(after_washing, correct_after_washing)\n    except AssertionError:\n        assert False, "after_washing should contain the rows of monthly >= handwashing_start" \n\ndef test_ax_exists():\n    assert \'ax\' in globals(), \\\n        "The result of the plot method should be assigned to a variable called ax"\n\n        \ndef test_plot_plots_correct_data():\n    y0_len = ax.get_lines()[0].get_ydata().shape[0]\n    y1_len = ax.get_lines()[1].get_ydata().shape[0]\n    assert (\n        (before_washing["proportion_deaths"].shape[0] == y0_len and\n         after_washing["proportion_deaths"].shape[0] == y1_len)\n        or\n        (before_washing["proportion_deaths"].shape[0] == y0_len and\n         after_washing["proportion_deaths"].shape[0] == y1_len)), \\\n        "The data in before_washing and after_washing should be plotted as two separate lines."')


# ## 7. More handwashing, fewer deaths?
# <p>Again, the graph shows that handwashing had a huge effect. How much did it reduce the monthly proportion of deaths on average?</p>




# Difference in mean monthly proportion of deaths due to handwashing
before_proportion = before_washing["proportion_deaths"]
after_proportion = after_washing["proportion_deaths"]
mean_diff = after_proportion.mean()-before_proportion.mean()
mean_diff





get_ipython().run_cell_magic('nose', '', '        \ndef test_before_proportion_exists():\n    assert \'before_proportion\' in globals(), \\\n        "before_proportion should be defined"\n        \ndef test_after_proportion_exists():\n    assert \'after_proportion\' in globals(), \\\n        "after_proportion should be defined"\n        \ndef test_mean_diff_exists():\n    assert \'mean_diff\' in globals(), \\\n        "mean_diff should be defined"\n        \ndef test_before_proportion_is_a_series():\n     assert hasattr(before_proportion, \'__len__\') and len(before_proportion) == 76, \\\n        "before_proportion should be 76 elements long, and not a single number."\n\ndef test_correct_mean_diff():\n    correct_before_proportion = before_washing["proportion_deaths"]\n    correct_after_proportion = after_washing["proportion_deaths"]\n    correct_mean_diff = correct_after_proportion.mean() - correct_before_proportion.mean()\n    assert mean_diff == correct_mean_diff, \\\n        "mean_diff should be calculated as the mean of after_proportion minus the mean of before_proportion."')


# ## 8. A Bootstrap analysis of Semmelweis handwashing data
# <p>It reduced the proportion of deaths by around 8 percentage points! From 10% on average to just 2% (which is still a high number by modern standards). </p>
# <p>To get a feeling for the uncertainty around how much handwashing reduces mortalities we could look at a confidence interval (here calculated using the bootstrap method).</p>



# A bootstrap analysis of the reduction of deaths due to handwashing
boot_mean_diff = []
for i in range(3000):
    boot_before = before_proportion.sample(frac=1, replace=True)
    boot_after = after_proportion.sample(frac=1, replace=True)
    boot_mean_diff.append( boot_after.mean() - boot_before.mean() )

# Calculating a 95% confidence interval from boot_mean_diff 
confidence_interval = pd.Series(boot_mean_diff).quantile([0.025, 0.975])
confidence_interval





get_ipython().run_cell_magic('nose', '', '\ndef test_confidence_interval_exists():\n    assert \'confidence_interval\' in globals(), \\\n        "confidence_interval should be defined"\n\ndef test_boot_before_correct_length():\n    assert len(boot_before) == len(before_proportion), \\\n        ("boot_before have {} elements and before_proportion have {}." + \n         "They should have the same number of elements."\n        ).format(len(boot_before), len(before_proportion))\n        \ndef test_confidence_interval_correct():\n    assert ((0.09 < abs(confidence_interval).max() < 0.11) and\n            (0.055 < abs(confidence_interval).min() < 0.075)) , \\\n        "confidence_interval should be calculated as the [0.025, 0.975] quantiles of boot_mean_diff."')


# ## 9. The fate of Dr. Semmelweis
# <p>So handwashing reduced the proportion of deaths by between 6.7 and 10 percentage points, according to a 95% confidence interval. All in all, it would seem that Semmelweis had solid evidence that handwashing was a simple but highly effective procedure that could save many lives.</p>
# <p>The tragedy is that, despite the evidence, Semmelweis' theory — that childbed fever was caused by some "substance" (what we today know as <em>bacteria</em>) from autopsy room corpses — was ridiculed by contemporary scientists. The medical community largely rejected his discovery and in 1849 he was forced to leave the Vienna General Hospital for good.</p>
# <p>One reason for this was that statistics and statistical arguments were uncommon in medical science in the 1800s. Semmelweis only published his data as long tables of raw data, but he didn't show any graphs nor confidence intervals. If he would have had access to the analysis we've just put together he might have been more successful in getting the Viennese doctors to wash their hands.</p>

# In[37]:


# The data Semmelweis collected points to that:
doctors_should_wash_their_hands = True



