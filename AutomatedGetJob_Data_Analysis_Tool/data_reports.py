import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def build_html_rpt(filepath, filename):

    pd.set_option('display.max_columns', None)
    #df = pd.read_csv('JOBLIST_09232020.csv', encoding='iso-8859-1', engine='python').sort_values(by=['Status', 'Start date', 'Start Time'])

    df = pd.read_csv(f'{filepath}/{filename}.txt', encoding='utf-8', engine='python').sort_values(by=['Status', 'StartDate', 'StartTime'])

    #Print list
    print(df.to_string())
    print('\n')
    #prints job and status amounts
    df2 = pd.crosstab(df['JobName'], df['Status']).sort_values(by='Canceled', ascending=False)
    print(df2.to_string())

    print('\n')
    #print date and status amounts
    df3 = pd.crosstab(df['StartDate'], df['Status'])
    print(df3.to_string())

    ax = sns.countplot(x='StartDate', hue='Status', palette='Set1', data=df)
    ax.set(title='End-of-Week Results', xlabel='Joblist')
    #plt.show()
    img_path = f'{filepath}/Job_Reports/{filename}_graphfile.png'
    plt.savefig(img_path, dpi=300)
    img_tag = f'<p><img src="{img_path}"> </p>'

    with open(f'{filepath}/Job_Reports/{filename}_Report.html', 'w', encoding='utf-8') as _file:
        _file.write('<center>'
                    +'<h1> Weekly Jobs Performance Report </h1><br><hr>'
                    + img_tag
                    +'<h2> Status Amt by Date </h2>' + df3.to_html(index=True, border=2, justify="center") + '<br><hr>'
                    +'<h2> Status Amt by Job </h2>' + df2.to_html(index=True, border=2, justify="center") + '<br><hr>'
                    +'<h2> Job List - Ordered by Date </h2>' + df.to_html(index=True, border=2, justify="center") + '<br><hr>'
                    +'</center>')

    print("Report Generated!")
#--End | github.com/eabdiel