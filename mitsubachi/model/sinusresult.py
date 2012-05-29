# -*- coding: utf-8 -*-
'''
@author: stransky
'''
#http://www.python.org/dev/peps/pep-0263/
import morphjongleur.model.experiment

class SinusExperiment(morphjongleur.model.experiment.Experiment):
    pass

class SinusResult(object):
    '''
    classdocs
    '''

    def __init__(self, voltage_trace, compartment, frequency, amplitude):
        '''
        Constructor
        '''
        self.morphology = voltage_trace.experiment.morphology
        self.morphology_name    = self.morphology.name
        self.compartment= compartment
        self.compartment_id = self.compartment.compartment_id
        self.frequency    = frequency
        self.amplitude    = amplitude
        self.v_maximum    = voltage_trace.v_max
        self.v_minimum    = voltage_trace.v_min
        self.t_maximum    = voltage_trace.t_max
        self.t_minimum    = voltage_trace.t_min
        self._phase_angle  = None

    @property
    def phase_angle(self):
        if not vars(self).has_key('_phase_angle') or self._phase_angle == None:
            self._biggest   = self.voltage_trace.t_max*self.frequency-(2.+ (0.25 if self.amplitude >0 else 0.75))  #based on max
        return self._biggest
    @phase_angle.setter
    def phase_angle(self, value):        raise AttributeError("cannot change calculated information")
    @phase_angle.deleter
    def phase_angle(self):               self._phase_angle   = None #del self._phase_angle

    def __str__(self):
        return '<%s(%s: experiment_key=%s, morphology_key=%s, t_min=%f [s],v_min=%f [mV], t_max=%f [s],v_max=%f [mV], f=%i Hz,phase angle=%f)>' % (
            self.__class__.__name__, str(self.result_key if vars().has_key('result_key') else ''), 
            str(self.experiment_key if vars().has_key('experiment_key') else ''),
            self.morphology_name,
            self.t_minimum,self.v_minimum,
            self.t_maximum,self.v_maximum,
            self.frequency,self.phase_angle
        )

    def __repr__(self):#TODO: creatable
        return '<%s(%s: experiment_key=%s, morphology_key=%s, t_min=%f [s],v_min=%f [mV], t_max=%f [s],v_max=%f [mV], f=%i Hz,phase angle=%f)>' % (
            self.__class__.__name__, str(self.result_key if vars().has_key('result_key') else ''), 
            str(self.experiment_key if vars().has_key('experiment_key') else ''),
            self.morphology_name,
            self.t_min,self.v_min,
            self.t_max,self.v_max,
            self.frequency,self.phase_angle
        )


def plot_duration_histogramm(sinus_results, morphology, frequency, picture_file=None, picture_formats=['png', 'pdf', 'svg']):  
    import matplotlib.pyplot

    x   = []
    for r in sinus_results:
        x.append( (r.t_maximum - r.t_minimum -  0.5 / r.frequency) * 1e3 )#[ms]

    matplotlib.pyplot.title('Delay at %i Hz in %s' % (frequency, morphology))
    matplotlib.pyplot.ylabel('#')
    #matplotlib.pyplot.ylim(0, 70)
    matplotlib.pyplot.xlabel('Delay [ms]')
    #matplotlib.pyplot.xlim(0, 2.5)
    matplotlib.pyplot.xticks()
    matplotlib.pyplot.grid(True, color='lightgrey')

    matplotlib.pyplot.hist(x, bins=20, normed=0, color='black')

    if(picture_file != None):
        for picture_format in picture_formats:
            matplotlib.pyplot.savefig(picture_file+'.'+picture_format,format=picture_format)
    else:
        matplotlib.pyplot.show()
    matplotlib.pyplot.close()

def plot_delay_histogramm(sinus_results, morphology, frequency, picture_file=None, picture_formats=['png', 'pdf', 'svg']):  
    import matplotlib.pyplot

    x   = []
    for r in sinus_results:
        delay = r.t_maximum - (0.75 / r.frequency)#soll maximum
        delay = delay - int( delay * r.frequency ) / r.frequency
        x.append( delay * 1e3 )#ms

    matplotlib.pyplot.title('Delay at %i Hz in %s' % (frequency, morphology))
    matplotlib.pyplot.xticks()
    matplotlib.pyplot.grid(True, color='lightgrey')

    matplotlib.pyplot.hist(x, bins=20, normed=0, color='black')
    matplotlib.pyplot.ylabel('#')
    matplotlib.pyplot.ylim(0, 300)
    matplotlib.pyplot.xlabel('Delay [ms]')
    matplotlib.pyplot.xlim(0, 1000./frequency)

    if(picture_file != None):
        for picture_format in picture_formats:
            matplotlib.pyplot.savefig(picture_file+'.'+picture_format,format=picture_format)
    else:
        matplotlib.pyplot.show()
    matplotlib.pyplot.close()

def plot_phaseshift_histogramm(sinus_results, morphology, frequency, picture_file=None, picture_formats=['png', 'pdf', 'svg']):  
    import matplotlib.pyplot

    x   = []
    for r in sinus_results:
        r.amplitude = -1e-9 #TODO: remove
        phase_angle = r.t_maximum*frequency-(2.+ (0.25 if r.amplitude >0 else 0.75))
        x.append(phase_angle if phase_angle > 0 else (phase_angle + 1))# < 0, falls aus vorheriger Schwingung

    matplotlib.pyplot.title('Phaseshift at %i Hz in %s' % (frequency, morphology))
    matplotlib.pyplot.grid(True, color='lightgrey')

    matplotlib.pyplot.hist(x, bins=20, normed=0, color='black')
    matplotlib.pyplot.ylabel('#')
    matplotlib.pyplot.ylim(0, 300)#
    matplotlib.pyplot.xlabel('Phaseangle [full circles]')
    matplotlib.pyplot.xlim(0, 1)

    if(picture_file != None):
        for picture_format in picture_formats:
            matplotlib.pyplot.savefig(picture_file+'.'+picture_format,format=picture_format)
    else:
        matplotlib.pyplot.show()
    matplotlib.pyplot.close()

def plot_voltage_histogramm(sinus_results, morphology, frequency, picture_file=None, picture_formats=['png', 'pdf', 'svg']):  
    import matplotlib.pyplot

    x   = []
    for r in sinus_results:
        x.append((r.v_maximum - r.v_minimum)/2.)

    matplotlib.pyplot.title('Amplitude at %i Hz in %s' % (frequency, morphology))
    matplotlib.pyplot.grid(True, color='lightgrey')

    matplotlib.pyplot.hist(x, bins=20, normed=0, color='black')
    matplotlib.pyplot.ylabel('#')
    matplotlib.pyplot.ylim(0, 130)#0.3
    matplotlib.pyplot.xlabel(u'ΔU [mV]')
    matplotlib.pyplot.xlim(0, 45)
 
    if(picture_file != None):
        for picture_format in picture_formats:
            matplotlib.pyplot.savefig(picture_file+'.'+picture_format,format=picture_format, widths=10)
    else:
        matplotlib.pyplot.show()
    matplotlib.pyplot.close()



def plot_delay_candlestick(sinus_results, morphology, picture_file=None, picture_formats=['png', 'pdf', 'svg']):
    import matplotlib.pyplot

    f   = {}
    for r in sinus_results:
        if not f.has_key(r.frequency):
            f[r.frequency] = []
        delay = r.t_maximum - (0.75 / r.frequency)#soll maximum
        delay = delay - int( delay * r.frequency ) / r.frequency
        f[r.frequency].append( delay * 1e3 )#ms

    matplotlib.pyplot.title('Delay in '+str(morphology))
    matplotlib.pyplot.xticks(rotation=90)#  range(1+len(data)),titles
    matplotlib.pyplot.grid(True, color='lightgrey')
 
    bp = matplotlib.pyplot.boxplot(f.values(), positions=f.keys(), widths=10)
    matplotlib.pyplot.ylabel('Delay [ms]')
    matplotlib.pyplot.ylim(0, 3)
    matplotlib.pyplot.xlabel('f [Hz]')
    matplotlib.pyplot.xlim(85, 510)
    #matplotlib.pyplot.setp(bp['whiskers'], color='k',  linestyle='-' )
    #matplotlib.pyplot.setp(bp['fliers'], color='k')

    if(picture_file != None):
        for picture_format in picture_formats:
            matplotlib.pyplot.savefig(picture_file+'.'+picture_format,format=picture_format)
    else:
        matplotlib.pyplot.show()
    matplotlib.pyplot.close()

def plot_phaseshift_candlestick(sinus_results, morphology, picture_file=None, picture_formats=['png', 'pdf', 'svg']):
    import matplotlib.pyplot

    f   = {}
    for r in sinus_results:
        if not f.has_key(r.frequency):
            f[r.frequency] = []
        r.amplitude = -1e-9 #TODO: remove
        phase_angle = r.t_maximum*r.frequency-(2.+ (0.25 if r.amplitude >0 else 0.75))
        f[r.frequency].append(phase_angle if phase_angle > 0 else (phase_angle + 1))# < 0, falls aus vorheriger Schwingung

    matplotlib.pyplot.title('Phaseshift in '+str(morphology))
    matplotlib.pyplot.xticks(rotation=90)#  range(1+len(data)),titles
    matplotlib.pyplot.grid(True, color='lightgrey')
 
    bp = matplotlib.pyplot.boxplot(f.values(), positions=f.keys(), widths=10)
    matplotlib.pyplot.ylabel('Phaseangle [full circles]')
    matplotlib.pyplot.ylim(0, 1)
    matplotlib.pyplot.xlabel('f [Hz]')
    #matplotlib.pyplot.xlim(85, 510)
    #matplotlib.pyplot.setp(bp['whiskers'], color='k',  linestyle='-' )
    #matplotlib.pyplot.setp(bp['fliers'], color='k')

    if(picture_file != None):
        for picture_format in picture_formats:
            matplotlib.pyplot.savefig(picture_file+'.'+picture_format,format=picture_format)
    else:
        matplotlib.pyplot.show()
    matplotlib.pyplot.close()
 
def plot_voltage_candlestick(sinus_results, morphology, picture_file=None, picture_formats=['png', 'pdf', 'svg']):
    import matplotlib.pyplot
    f   = {}
    for r in sinus_results:
        if not f.has_key(r.frequency):
            f[r.frequency] = []
        f[r.frequency].append((r.v_maximum - r.v_minimum)/2.)

    matplotlib.pyplot.title('Amplitude in '+str(morphology))
    matplotlib.pyplot.xticks(rotation=90)#  range(1+len(data)),titles
    matplotlib.pyplot.grid(True, color='lightgrey')
    
    bp = matplotlib.pyplot.boxplot(f.values(), positions=f.keys(), widths=10)
    matplotlib.pyplot.ylabel(u'ΔU [mV]')
    matplotlib.pyplot.ylim(0, 40)
    matplotlib.pyplot.xlabel('f [Hz]')
    #matplotlib.pyplot.xlim(85, 510)
    #matplotlib.pyplot.setp(bp['whiskers'], color='k',  linestyle='-' )
    #matplotlib.pyplot.setp(bp['fliers'], color='k')

    if(picture_file != None):
        for picture_format in picture_formats:
            matplotlib.pyplot.savefig(picture_file+'.'+picture_format,format=picture_format)
    else:
        matplotlib.pyplot.show()
    matplotlib.pyplot.close()


if __name__ == '__main__':
    from morphjongleur.io.database import Database
    db = Database(
                db_name='postgresql://hal08.g-node.pri/morphjongleur',
                exec_role='morphjokey_admin',
                exec_path='mitsubachi'
            )
    # must be mapped before Object is created
    import morphjongleur.orm.sinusresult
    mapping = morphjongleur.orm.sinusresult.Mapper( db )
    mapping.orm_map()
    mapping.create_tables()
    
    picture_formats=['svg']#'png', 
    for m in ['H060602DB_10_2_zentai_','H060607DB_10_2(zentai)','H060602VB_10_2_zentai_','H060607VB_10_2(zentai)']:#'test', 
        print m,
        print "\t",
        results = []
        for f in range(100,501,15):#(10,701,15) TODO: get from DB group by ... 
            results_f = mapping.load_experiment(m, f)
            try:
                plot_delay_histogramm(      results_f, m, f, '/tmp/delay_histogramm_%s%iHz'    %(m,f), picture_formats )
                plot_phaseshift_histogramm( results_f, m, f, '/tmp/phase_histogramm_%s%iHz'    %(m,f), picture_formats )
                plot_voltage_histogramm(    results_f, m, f, '/tmp/voltage_histogramm_%s%iHz'  %(m,f), picture_formats )
                plot_duration_histogramm(   results_f, m, f, '/tmp/duration_histogramm_%s%iHz' %(m,f), picture_formats )
                print f,  
            except IndexError, te:
                pass
            except Exception, e:
                import traceback
                print traceback.format_exc()
            results.extend(results_f)
        try:
            plot_delay_candlestick(      results, m, '/tmp/delay_candlestick_%s' %(m),  picture_formats )
            plot_voltage_candlestick(    results, m, '/tmp/voltage_candlestick_%s'%(m), picture_formats )
            plot_phaseshift_candlestick( results, m, '/tmp/phase_candlestick_%s' %(m),  picture_formats )
            print ''
        except IndexError, te:
            pass
        except Exception, e:
            import traceback
            print traceback.format_exc()
