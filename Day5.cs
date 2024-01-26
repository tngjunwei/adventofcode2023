using NPOI.HSSF.Record.Chart;
using NPOI.SS.Formula.PTG;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

// Port-over from day5.py
// C# is approx 20 times faster than Python.
// Python will require several hours for N=1e9, whereas
// C# only requires 20min.

namespace Playground
{
    using longerval = Tuple<long, long>;
    using Mapping = Tuple<long, long, long>;
    public class Day5
    {
        private string[] Data;
        public Day5(string path)
        {
            this.Data = File.ReadAllLines(path);
        }

        public void Solve()
        {
            List<longerval> listOfSeeds = ProcessNewSeeds(Data[0]);
            List<List<Mapping>> listOfRawMaps = ProcessMaps(Data.SubArray(2, Data.Length - 2));
            List<Map> listOfMaps = new List<Map>();

            foreach(var map in listOfRawMaps)
            {
                listOfMaps.Add(new Map(map));
            }

            long minLocation = long.MaxValue;
            foreach(var seedRange in listOfSeeds)
            {
                var start = DateTime.Now;

                for(long i = seedRange.Item1; i <= seedRange.Item2; i++)
                {
                    long curr = i;
                    foreach(var map in listOfMaps)
                    {
                        curr = map.Convert(curr);
                    }
                    minLocation = Math.Min(minLocation, curr);
                }
                var end = DateTime.Now;
                Console.WriteLine($"{seedRange.Item2-seedRange.Item1} entries took {end-start} seconds: {minLocation}");
            }

            Console.WriteLine($"Solution is {minLocation}");
        }

        private List<longerval> ProcessNewSeeds(string row)
        {
            string num_list_str = row.Split(":")[1].Trim();
            string[] rawNums = num_list_str.Split(" ");

            List<long> listOfNums = new List<long>();
            foreach (var rawNum in rawNums)
                listOfNums.Add(long.Parse(rawNum));

            List<longerval> listOflongervals = new List<longerval>();
            for(int i = 0; i < listOfNums.Count; i += 2)
            {
                listOflongervals.Add(new longerval(listOfNums[i], listOfNums[i] + listOfNums[i + 1] - 1));
            }

            return listOflongervals;
        }

        private List<List<Mapping>> ProcessMaps(string[] data)
        {
            List<List<Mapping>> listOfMaps = new List<List<Mapping>>();
            List<Mapping> mappings = new List<Mapping>();

            foreach (var s in data)
            {
                var row = s.Trim();
                if (row.Length == 0)
                {
                    listOfMaps.Add(mappings);
                    continue;
                }

                if (row.EndsWith(":"))
                {
                    mappings = new List<Mapping>();
                }
                else
                {
                    var tmp = row.Split(" ");
                    Mapping mapping = new Mapping(long.Parse(tmp[0].Trim()),
                                                  long.Parse(tmp[1].Trim()),
                                                  long.Parse(tmp[2].Trim()));
                    mappings.Add(mapping);
                }
            }

            if (mappings.Count > 0)
                listOfMaps.Add(mappings);
            return listOfMaps;
        }
    }

    public class Map
    {
        private List<Mapping> Mappings;
        public Map(List<Mapping> rawMaps)
        {
            Mappings = new List<Mapping>();
            foreach(Mapping map in rawMaps)
            {
                var (dest, src, dist) = map;
                var entry = new Mapping(src, src + dist - 1, dest);
                Mappings.Add(entry);
            }

            Mappings.Sort();
        }

        public long Convert(long srcId)
        {
            int idx = BinarySearch(0, Mappings.Count - 1, srcId);
            if (idx == -1)
                return srcId;
            else
            {
                var (src, _, dest) = Mappings[idx];
                return dest + (srcId - src);
            }
        }

        private int BinarySearch(int l, int r, long toFind)
        {
            if (l > r) return -1;

            int m = l + (r - l) / 2;
            long start = Mappings[m].Item1;
            long end = Mappings[m].Item2;

            if (start <= toFind && toFind <= end) return m;

            if (toFind < start) return BinarySearch(l, m - 1, toFind);
            else if (toFind > end) return BinarySearch(m + 1, r, toFind);

            return -1;
        }
    }

    public static class Extensions
    {
        public static T[] SubArray<T>(this T[] array, int offset, int length)
        {
            return array.Skip(offset).Take(length).ToArray();
        }
    }
}
