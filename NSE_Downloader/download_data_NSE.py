##############################################################################

def get_NSE_data(symbol, start_date, end_date):
    
    # Convert string to date format
    start = datetime.strptime(start_date, '%Y-%m-%d').date()
    end = datetime.strptime(end_date, '%Y-%m-%d').date()

    inputData = pandas.DataFrame()
    
    # Creating loop which will extract data from NSE site year by year
    temp_start = start
    while temp_start <= end:
        if temp_start + timedelta(364) >= end:
            print('Part I: temp_start: ', temp_start, ' end :', end)
            print('--------------------------------------------------')
            inputData = inputData.append(download_data(symbol, temp_start, end))                
        else:
            temp_end = temp_start + timedelta(364)
            print('Part II: temp_start: ', temp_start, ' temp_end: ', temp_end)
            print('--------------------------------------------------')
            inputData = inputData.append(download_data(symbol, temp_start, temp_end))
            
        temp_start = temp_start + timedelta(365)
        
    print(len(inputData), "--------------")
    return inputData

##############################################################################

def download_data(Ticker, start_date, end_date):
    
    url = 'http://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?' + \
      'symbol=' + Ticker + \
      '&segmentLink=3&symbolCount=1&series=ALL&' + \
      'dateRange=' + '' + \
      '+&fromDate=' + start_date.strftime('%d-%m-%Y') + \
      '&toDate=' + end_date.strftime('%d-%m-%Y') + \
      '&dataType=PRICEVOLUMEDELIVERABLE'

    # Generate data by requesting the URL above    
    page_content = requests.get(url)
    
    if page_content.status_code == 200:
        
        # Page content parsed through BeautifulSoup
        page = BeautifulSoup(page_content.content)
        fileName = os.path.join(Ticker, \
                                Ticker + '_' + start_date.strftime('%d-%m-%Y') + '_' \
                                             + end_date.strftime('%d-%m-%Y') + '.csv')
        
        # Extracting Link from the page loaded above and downloading file 
        with open(fileName, 'wb') as handle:
            data = requests.get('http://www.nseindia.com' + page.find('a').get('href'), \
                                 stream = True)
    
            # Downloading file
            for block in data.iter_content(1024):
                handle.write(block)
      
        return pandas.read_csv(fileName)

    else:
        print('\nError getting data from the website\n')
        return pandas.DataFrame()
    

##############################################################################