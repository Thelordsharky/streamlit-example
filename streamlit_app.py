
git clone git@github.com:hannorein/oec_plots.git
cd oec_plots
git submodule init
git submodule update
#!/usr/bin/python
import xml.etree.ElementTree as ET
import subprocess, glob, os, datetime

# Open pipe gnuplot. You may want to change the terminal from svg to pdf for publication quality plots.
gnuplot = subprocess.Popen(['gnuplot',"-persist"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
gnuplot.stdin.write("""
set terminal svg
set output "plot_mass_vs_semimajoraxis_discovery.svg"
set xlabel "Semi-major axis [AU]"
set ylabel "Planet mass [MJupiter]"
set logscale xy
set xrange [0.001:50]
set yrange [0.008:350]
set key top left
set label "Data taken from the Open Exoplanet Catalogue. Last updated on """+datetime.date.today().isoformat()+"""." at screen 0.31,0.15 front font ",8"
plot \
"-" with point pt 7 lc 2 t "Radial velocity planets", \
"-" with point pt 7 lc 3 t "Transiting planets",  \
"-" with point pt 7 lc 1 t "Directly imaged planets", \
"-" with point pt 7 lc 4 t "Microlensing planets"
""")

def plotPlanetWithDiscoveryMethod(_discoverymethod):
	for filename in glob.glob("open_exoplanet_catalogue/systems/*.xml"):
		system = ET.parse(open(filename, 'r'))
		planets = system.findall(".//planet")
		for planet in planets:
			try:
				mass = float(planet.findtext("./mass"))
				semimajoraxis = float(planet.findtext("./semimajoraxis"))
				discoverymethod = planet.findtext("./discoverymethod")
				if discoverymethod==_discoverymethod:
					gnuplot.stdin.write("%e\t%e\n"%(mass, semimajoraxis))
			except:
				# Most likely cause for an exception: Mass or semi-major axis not specified for this planet.
				# One could do a more complicated check here and see if the period and the mass of the host star is given and then calculate the semi-major axis 
				pass
	gnuplot.stdin.write("\ne\n")

plotPlanetWithDiscoveryMethod("RV")
plotPlanetWithDiscoveryMethod("transit")
plotPlanetWithDiscoveryMethod("imaging")
plotPlanetWithDiscoveryMethod("microlensing")

gnuplot.stdin.close()

