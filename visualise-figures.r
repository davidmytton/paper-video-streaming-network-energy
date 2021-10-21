#####
## ##  CODE TO VISUALISE THE FIGURES FROM 'THE NETWORK ENERGY INTENSITY OF VIDEO STREAMING OVER WI-FI AND 4G'
#####
  #
  #     IAIN STAFFELL ~ 2021
  #
#####


	boxplot.pars = list(
        boxfill = '#FFEBAD', 
        whisklty=1
    )

    point.colour = '#371AEA44'

    gg = function()
    {
        par(bg='white')
        par(mar=c(2.5, 3, 2, 1))
        par(tck=0.01)
        par(mgp=c(1.75, 0.5, 0))
        par(font.lab=2)
        par(las=1)
        par(xaxs='i', yaxs='i')
        par(cex=1.15)
    }

    dev.new(height=6, width=7)
    gg()

    options(stringsAsFactors=TRUE)

#####
## ##  FIGURE 2
#####

    data = read.csv('traceroute-samples/traceroute-samples.csv')

    data = data.frame(
        cnt = data$Participant.Country,
        con = data$Connection,
        hop = data$Trace.Hop.Count
    )

    UK = data$cnt == 'uk'
    WF = data$con == 'wifi'

    data = rbind(
        data.frame(hop=data$hop[UK      ], type='\nUK\n(all)'),
        data.frame(hop=data$hop[UK & !WF], type='\nUK\n(4G)'),
        data.frame(hop=data$hop[UK &  WF], type='\nUK\n(WiFi)'),
        data.frame(hop=data$hop[        ], type='\nGlobal\n(all)'),
        data.frame(hop=data$hop[     !WF], type='\nGlobal\n(4G)'),
        data.frame(hop=data$hop[      WF], type='\nGlobal\n(WiFi)')
    )

    boxplot(data$hop ~ data$type, pars=boxplot.pars, ylim=c(0,19), ylab='Hop count', range=0)
    axis(4, labels=FALSE)

    xx = jitter( as.numeric(data$type) )
    points(xx, data$hop, lwd=2, col=point.colour)

    dev.print(pdf, 'fig2.pdf', height=6, width=7, paper='special')




#####
## ##  FIGURE 3
#####

    data = read_data('model/figures/fig3.csv')

    data = rbind(
        data.frame(hop=data$`All`, type='All'),
        data.frame(hop=data$`ISP`, type='ISP'),
        data.frame(hop=data$`Google or Facebook`, type='Google or\nFacebook')
    )

    boxplot(data$hop ~ data$type, pars=boxplot.pars, ylim=c(0,19), ylab='Hop count', range=0)
    axis(4, labels=FALSE)

    xx = jitter( as.numeric(data$type) )
    points(xx, data$hop, lwd=2, col=point.colour)

    dev.print(pdf, 'fig3.pdf', height=6, width=7, paper='special')




#####
## ##  FIGURE 4
#####

    data = read_data('model/figures/fig4.csv')

    data = rbind(
        data.frame(hop=data$`4G` / 1000, type='4G'),
        data.frame(hop=data$`Wi-Fi` / 1000, type='WiFi'),
        data.frame(hop=data$`Total` / 1000, type='Total')
    )

    par(mar=c(2.5, 3, 2, 4))

    boxplot(data$hop ~ data$type, pars=boxplot.pars, ylim=c(0,6), ylab='Electricity consumed (TWh/year)', range=0)

    GB = 324.8
    axis(4, at=c(0,0.25,0.5,0.75,1,1.25,1.5,1.75)*GB/100, labels=c('0%', '0.25%', '0.5%', '0.75%', '1%', '1.25%', '1.5%', '1.75%'))
    mtext(side=4, line=2.85, 'Share of national electricity demand', font=2, las=0)


    dev.print(pdf, 'fig4.pdf', height=6, width=7, paper='special')

    par(mar=c(2.5, 3, 2, 1))
 




#####
## ##  FIGURE 5
#####

    data = read_data('model/figures/fig5-left.csv')

    left = rbind(
        data.frame(hop=data$`Edge`, type='Edge'),
        data.frame(hop=data$`Metro`, type='Metro'),
        data.frame(hop=data$`Core`, type='Core')
    )

    data = read_data('model/figures/fig5-right.csv')

    right = rbind(
        data.frame(hop=data$`Edge`, type='Edge'),
        data.frame(hop=data$`Metro`, type='Metro'),
        data.frame(hop=data$`Core`, type='Core')
    )

    layout(t(1:2))
    par(cex=1.15)

    boxplot(left$hop ~ left$type, pars=boxplot.pars, ylim=c(0,75), ylab='Electricity consumed (GWh/year)', range=0, yaxt='n')
    axis(2, at=seq(0,75,15))
    axis(4, at=seq(0,75,15), labels=FALSE)

    boxplot(right$hop ~ right$type, pars=boxplot.pars, ylim=c(0,250), ylab='Electricity consumed (GWh/year)', range=0)
    axis(4, labels=FALSE)

    dev.print(pdf, 'fig5.pdf', height=6, width=14, paper='special')


