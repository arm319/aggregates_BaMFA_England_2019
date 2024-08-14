import numpy as np
import matplotlib.pyplot as plt
import arviz as az
import pandas as pd

def filelabeler(useratiodata):
    if useratiodata==1:
        scenario='scenarioB'
    if useratiodata!=1:
        scenario='scenarioA'
    return scenario

def ppplots(posterior_pred,datavector,stockindex,flowindex,CoMindex,useratiodata):

    """
    Function for producing posterior predictive plots, for change in stock, flow data and conservation of mass conditions

    Arguments:
        posterior_pred: posterior predictive samples
        datavector: vector of data values for flow and change in stock values, as well as 0 for each conservation of mass conditions
        stockindex,flowindex,CoMindex: indices of datavector that splits it into stock data, flow data and conservation of mass conditions respectively
        userratiodata: whether to use ratio data, to split scenario A and B

    """

    plt.rcParams.update({'font.size': 18})

    stocktally = 0 * datavector[stockindex]
    flowtally = 0 * datavector[flowindex]
    CoMtally = 0 * datavector[CoMindex]

    for i in range(0, posterior_pred['stockdata'].shape[0]):
        stocktally = stocktally + (posterior_pred['stockdata'][i, :] > datavector[stockindex])
        flowtally = flowtally + (posterior_pred['flowdata'][i, :] > datavector[flowindex])
        CoMtally = CoMtally + (posterior_pred['CoM'][i, :] > datavector[CoMindex])


    # plot p-values
    plt.stem(stocktally / posterior_pred['stockdata'].shape[0], basefmt=" ")
    plt.ylabel('p value')
    plt.title('Stock data p values')
    plt.xticks([])
    plt.savefig('outputgraphs' + filelabeler(useratiodata) + '/' + 'stockpvalues' + filelabeler(useratiodata) + '.pdf', bbox_inches="tight")
    plt.show()

    plt.stem(flowtally / posterior_pred['stockdata'].shape[0], basefmt=" ")
    plt.ylabel('p value')
    plt.title('Flow data p values')
    plt.xticks([])
    plt.savefig('outputgraphs' + filelabeler(useratiodata) + '/' + 'flowpvalues' + filelabeler(useratiodata) + '.pdf', bbox_inches="tight")
    plt.show()

    plt.stem(CoMtally / posterior_pred['stockdata'].shape[0], basefmt=" ")
    plt.ylabel('p value')
    plt.title('CoM p values')
    plt.xticks([])
    plt.savefig('outputgraphs' + filelabeler(useratiodata) + '/' + 'CoMpvalues' + filelabeler(useratiodata) + '.pdf', bbox_inches="tight")
    plt.show()

    stock_hdi = az.hdi(posterior_pred['stockdata'], hdi_prob=0.95)
    flow_hdi = az.hdi(posterior_pred['flowdata'], hdi_prob=0.95)
    CoM_hdi = az.hdi(posterior_pred['CoM'], hdi_prob=0.95)

    checkcoveragestocks = (stock_hdi[:, 0] <= datavector[stockindex]) & (datavector[stockindex] <= stock_hdi[:, 1])
    checkcoverageflows = (flow_hdi[:, 0] <= datavector[flowindex]) & (datavector[flowindex] <= flow_hdi[:, 1])
    checkcoverageCoM = (CoM_hdi[:, 0] <= datavector[CoMindex]) & (datavector[CoMindex] <= CoM_hdi[:, 1])

    datavectorstocks = np.reshape(datavector[stockindex], (datavector[stockindex].size, 1))

    datavectorflows = np.reshape(datavector[flowindex], (datavector[flowindex].size, 1))

    datavectorCoM = np.reshape(datavector[CoMindex], (datavector[CoMindex].size, 1))

    checkcoveragestocks = np.reshape(checkcoveragestocks, (checkcoveragestocks.size, 1))

    checkcoverageflows = np.reshape(checkcoverageflows, (checkcoverageflows.size, 1))

    checkcoverageCoM = np.reshape(checkcoverageCoM, (checkcoverageCoM.size, 1))

    print('check stock data coverage')
    print(np.hstack((stock_hdi, datavectorstocks, checkcoveragestocks)))

    print('check flow data coverage')
    print(np.hstack((flow_hdi, datavectorflows, checkcoverageflows)))

    print('check CoM coverage')
    print(np.hstack((CoM_hdi, datavectorCoM, checkcoverageCoM)))

    plt.plot(stock_hdi[:, 0], linestyle='None', marker='_', color='red')
    plt.plot(stock_hdi[:, 1], linestyle='None', marker='_', color='red')
    plt.plot(datavector[stockindex], linestyle='None', marker='.')
    plt.plot((range(0, stock_hdi[:, 0].size), range(0, stock_hdi[:, 0].size)), (stock_hdi[:, 0], stock_hdi[:, 1]),color='black', linewidth=0.5)
    plt.title('Stock data 95% HDI of PPD')
    plt.xticks([])
    plt.savefig('outputgraphs' + filelabeler(useratiodata) + '/' + 'stockpredictivehdi' + filelabeler(useratiodata) + '.pdf',bbox_inches="tight")
    plt.show()

    #plot posterior predictive 95% HDI
    plt.plot(flow_hdi[:, 0], linestyle='None', marker='_', color='red')
    plt.plot(flow_hdi[:, 1], linestyle='None', marker='_', color='red')
    plt.plot(datavector[flowindex], linestyle='None', marker='.')
    plt.plot((range(0, flow_hdi[:, 0].size), range(0, flow_hdi[:, 0].size)), (flow_hdi[:, 0], flow_hdi[:, 1]),
             color='black', linewidth=0.5)
    plt.title('Flow data 95% HDI of PPD')
    plt.xticks([])
    plt.savefig('outputgraphs' + filelabeler(useratiodata) + '/' + 'flowpredictivehdi' + filelabeler(useratiodata) + '.pdf',
                bbox_inches="tight")
    plt.show()

    plt.plot(CoM_hdi[:, 0], linestyle='None', marker='_', color='red')
    plt.plot(CoM_hdi[:, 1], linestyle='None', marker='_', color='red')
    plt.plot(datavector[CoMindex], linestyle='None', marker='.')
    plt.plot((range(0, CoM_hdi[:, 0].size), range(0, CoM_hdi[:, 0].size)), (CoM_hdi[:, 0], CoM_hdi[:, 1]),
             color='black', linewidth=0.5)
    plt.title('CoM 95% HDI of PPD')
    plt.xticks([])
    plt.savefig('outputgraphs' + filelabeler(useratiodata) + '/' + 'CoMpredictivehdi' + filelabeler(useratiodata) + '.pdf',
                bbox_inches="tight")
    plt.show()

    columns = ['Data_value', '95%_HDI_lower', '95%_HDI_higher', 'p_value']

    stockdatappd = np.column_stack((datavector[stockindex],stock_hdi[:, 0],stock_hdi[:, 1],stocktally / posterior_pred['stockdata'].shape[0]))

    flowdatappd = np.column_stack((datavector[flowindex], flow_hdi[:, 0], flow_hdi[:, 1], flowtally / posterior_pred['stockdata'].shape[0]))

    CoMdatappd = np.column_stack((datavector[CoMindex], CoM_hdi[:, 0], CoM_hdi[:, 1], CoMtally / posterior_pred['stockdata'].shape[0]))

    stockdatappd = pd.DataFrame(stockdatappd, columns=columns)

    flowdatappd = pd.DataFrame(flowdatappd, columns=columns)

    CoMdatappd = pd.DataFrame(CoMdatappd, columns=columns)

    stockdatappd.to_csv('stockdatappd'+filelabeler(useratiodata)+'.csv', index=False)
    flowdatappd.to_csv('flowdatappd'+filelabeler(useratiodata)+'.csv', index=False)
    CoMdatappd.to_csv('CoMdatappd'+filelabeler(useratiodata)+'.csv', index=False)

def ppplotsratiodata(posterior_pred,ratiovector,useratiodata):

    """
    Function for producing posterior predictive plots, for ratio data

    Arguments:
        posterior_pred: posterior predictive samples
        ratiovector: vector of ratio data values
        userratiodata: whether to use ratio data, to split scenario A and B

    """

    ratiotally = 0 * np.array(ratiovector)


    for i in range(0, posterior_pred['stockdata'].shape[0]):
        ratiotally = ratiotally + (posterior_pred['ratiodata'][i, :] > ratiovector)

    #plot p-values
    plt.stem(ratiotally / posterior_pred['stockdata'].shape[0], basefmt=" ")
    plt.ylabel('p value')
    plt.title('ratio data p values')
    plt.xticks([])
    plt.savefig('outputgraphs' + filelabeler(useratiodata) + '/' + 'ratiopvalues' + filelabeler(useratiodata) + '.pdf',
                bbox_inches="tight")
    plt.show()

    ratio_hdi = az.hdi(posterior_pred['ratiodata'], hdi_prob=0.95)
    checkcoverageratio = (ratio_hdi[:, 0] <= ratiovector) & (ratiovector <= ratio_hdi[:, 1])
    datavectorratio = np.reshape(ratiovector, (ratiovector.size, 1))
    checkcoverageratio = np.reshape(checkcoverageratio, (checkcoverageratio.size, 1))

    print('check ratio data coverage')
    print(np.hstack((ratio_hdi, datavectorratio, checkcoverageratio)))

    #plot posterior predictive 95% hdi
    plt.plot(ratio_hdi[:, 0], linestyle='None', marker='_', color='red')
    plt.plot(ratio_hdi[:, 1], linestyle='None', marker='_', color='red')
    plt.plot(ratiovector, linestyle='None', marker='.')
    plt.plot((range(0, ratio_hdi[:, 0].size), range(0, ratio_hdi[:, 0].size)), (ratio_hdi[:, 0], ratio_hdi[:, 1]),
             color='black', linewidth=0.5)
    plt.title('ratio data 95% HDI of PPD')
    plt.xticks([])
    plt.savefig(
        'outputgraphs' + filelabeler(useratiodata) + '/' + 'ratiopredictivehdi' + filelabeler(useratiodata) + '.pdf',
        bbox_inches="tight")
    plt.show()

    columns = ['Data_value', '95%_HDI_lower', '95%_HDI_higher', 'p_value']

    ratiodatappd=np.column_stack((ratiovector,ratio_hdi[:, 0],ratio_hdi[:, 1],ratiotally / posterior_pred['stockdata'].shape[0]))

    ratiodatappd = pd.DataFrame(ratiodatappd, columns=columns)

    ratiodatappd.to_csv('ratiodatappd'+filelabeler(useratiodata)+'.csv', index=False)

def top10hdi(trace,processnamesdict,availablechildstocksandflows,useratiodata,m):

    """
    Function for plotting the top 10 variables with the widest highest density interval width

    Arguments:
        trace: samples from the posterior distribution
        processnamesdict: dictionary of stock and flow names to label the graphs
        availablechildstocksandflows: list of indices to denote flow and change in stock variables that are non zero in the system
        userratiodata: whether to use ratio data, to split scenario A and B
        m: number of processes

    """

    ci_95 = az.hdi(trace, hdi_prob=0.95)
    ci_95_juststocks = az.hdi(trace['posterior'].stocks, hdi_prob=0.95)
    ci_95_justflows = az.hdi(trace['posterior'].flows, hdi_prob=0.95)

    ci_95_juststocks_length = ci_95_juststocks['stocks'][:, 1] - ci_95_juststocks['stocks'][:, 0]
    ci_95_justflows_length = ci_95_justflows['flows'][:, 1] - ci_95_justflows['flows'][:, 0]
    ci_95_length = np.hstack((ci_95_juststocks_length, ci_95_justflows_length))

    plt.rcParams.update({'font.size': 10})

    posteriorhdilargesttosmallest = np.array(ci_95_length).argsort().tolist()[::-1]


    processnamesdict1 = processnamesdict
    processnamesdict1['-1'] = 'Stock'

    quotient4 = [[i // m - 1, i % m] for i in np.array(availablechildstocksandflows)[posteriorhdilargesttosmallest]]

    def conj(x):
        if x=='-1':
            ans='of'
        else:
            ans='to'
        return ans

    quotient4names = [processnamesdict1[str(i // m - 1)] +' '+conj(str(i // m - 1))+' '+processnamesdict1[str(i % m)] for i in
                      np.array(availablechildstocksandflows)[posteriorhdilargesttosmallest]]

    #plot top 10 posterior 95% HDI lengths
    plt.plot(quotient4names[0:10], ci_95_length[posteriorhdilargesttosmallest][0:10])

    plt.xticks(rotation=90)
    plt.title('Top 10 95% HDI lengths of marginal posterior distributions')
    plt.ylabel('HDI length')
    plt.savefig('outputgraphs' + filelabeler(useratiodata) + '/' + 'top10largesthdi' + filelabeler(useratiodata) + '.pdf',
                bbox_inches="tight")
    plt.show()

    columns = ['Variable Name', '95%_HDI_width']

    top10hdidata = np.column_stack((quotient4names[0:10],ci_95_length[posteriorhdilargesttosmallest][0:10]))

    top10hdidata = pd.DataFrame(top10hdidata, columns=columns)

    top10hdidata.to_csv('top10hdidata'+filelabeler(useratiodata)+'.csv', index=False)

    return ci_95_length
