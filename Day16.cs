// C# not required if used the directionalEnergisedSet trick
using NPOI.POIFS.Crypt.Dsig;
using NPOI.SS.Formula.Functions;
using NPOI.Util;
using System;
using System.Collections.Generic;
using System.Diagnostics.Metrics;
using System.Drawing.Printing;
using System.IO;
using System.Linq;
using System.Security.Policy;
using System.Text;
using System.Threading.Tasks;

namespace Playground
{
    using PairInt = Tuple<int, int>;
    public static class Resource
    {
        public static Dictionary<char, Dictionary<PairInt, PairInt>> ReflectionMap = new Dictionary<char, Dictionary<PairInt, PairInt>>()
        {
            { '/', new Dictionary<PairInt,PairInt> {
                { Tuple.Create(0,1), Tuple.Create(-1,0) },
                { Tuple.Create(1,0), Tuple.Create(0,-1) },
                { Tuple.Create(0,-1), Tuple.Create(1,0) },
                { Tuple.Create(-1,0), Tuple.Create(0,1) }
            } },
            { '\\', new Dictionary<PairInt, PairInt>
            {
                { Tuple.Create(0,1), Tuple.Create(1,0) },
                { Tuple.Create(1,0), Tuple.Create(0,1) },
                { Tuple.Create(0,-1), Tuple.Create(-1,0) },
                { Tuple.Create(-1,0), Tuple.Create(0,-1) }
            } },
        };
    }

    public class Ray
    {
        private PairInt Position { get; set; }
        private PairInt DirectionVector { get; set;}
        private bool Dead { get; set; }

        public Ray(PairInt pos, PairInt dirVector)
        {
            Position = pos;
            DirectionVector = dirVector;
            Dead = false;
        }

        public bool IsDead() => Dead;

        private Ray? GetNextState(string[] grid)
        {
            var (dr, dc) = DirectionVector;
            var (r, c) = Position;
            char symbol = grid[r][c];

            PairInt newDirectionVector = DirectionVector.Copy();
            Ray? newRay = null;

            if (symbol == '.')
                newDirectionVector = DirectionVector.Copy();
            else if (symbol == '-')
            {
                if (dr != 0)
                {
                    newRay = new Ray(Position.Copy(), Tuple.Create(0, -1));
                    newDirectionVector = Tuple.Create(0, 1);
                }
            }
            else if (symbol == '|')
            {
                if (dc != 0)
                {
                    newRay = new Ray(Position.Copy(), Tuple.Create(-1, 0));
                    newDirectionVector = Tuple.Create(1, 0);
                }
            }
            else
            {
                newDirectionVector = Resource.ReflectionMap[symbol][DirectionVector];
            }
            DirectionVector = newDirectionVector;

            return newRay;
        }

        public Ray? Move(string[] grid, HashSet<PairInt> energisedSet, HashSet<Tuple<PairInt, PairInt>> directionalEnergisedSet)
        {
            int M = grid.Length, N = grid[0].Length;
            var (r, c) = Position;
            var (dr, dc) = DirectionVector;

            Ray? newRay = null;
            int new_r = r + dr, new_c = c + dc;
            if(0 <= new_r && new_r < M && 0 <= new_c && new_c < N)
            {
                Tuple<PairInt, PairInt> directionalInfo = Tuple.Create(
                    Tuple.Create(new_r, new_c), DirectionVector);

                if (directionalEnergisedSet.Contains(directionalInfo))
                {
                    Dead = true;
                    return newRay;
                } else
                {
                    directionalEnergisedSet.Add(directionalInfo);
                }
                Position = Tuple.Create(new_r, new_c);
                energisedSet.Add(Tuple.Create(new_r, new_c));
                newRay = GetNextState(grid);
            }
            else
            {
                Dead = true;
            }

            return newRay;
        }
    }

    public static class Solver
    {
        public static int Simulate(string[] grid, PairInt startPos, PairInt initDir)
        {
            Ray ray = new Ray(startPos, initDir);
            Queue<Ray> queue = new Queue<Ray>();
            queue.Enqueue(ray);
            HashSet<PairInt> energisedSet = new HashSet<PairInt>();
            HashSet<Tuple<PairInt,PairInt>> specificEnergisedSet = new HashSet<Tuple<PairInt, PairInt>>();
            int sameNumLimit = 10;
            int count = 0;

            while (queue.Any())
            {
                int before = energisedSet.Count;

                int N = queue.Count;
                for(int i=0; i < N; i++)
                {
                    Ray currRay = queue.Dequeue();
                    Ray? newRay = currRay.Move(grid, energisedSet, specificEnergisedSet);

                    if (newRay != null) queue.Enqueue(newRay);
                    if (!currRay.IsDead()) queue.Enqueue(currRay);
                }

                int after = energisedSet.Count;
                if(after == before)
                {
                    count++;
                } else
                {
                    count = 0;
                }

                if (count > sameNumLimit)
                    break;
            }

            return energisedSet.Count;
        }

        public static string[] GetData(string path)
        {
            return File.ReadAllLines(path);
        }

        public static int Solve(string path)
        {
            string[] grid = GetData(path);
            //grid = new string[]
            //{
            //    ".|...\\....",
            //    "|.-.\\.....",
            //    ".....|-...",
            //    "........|.",
            //    "..........",
            //    ".........\\",
            //    "..../.\\\\..",
            //    ".-.-/..|..",
            //    ".|....-|.\\",
            //    "..//.|...."
            //};
            
            //PairInt startPos = Tuple.Create(0, -1);
            //PairInt initDir = Tuple.Create(0, 1);

            List<int> listOfRes = new List<int>();
            List<PairInt> listOfStartPos = new List<PairInt>();
            List<PairInt> listOfInitDir = new List<PairInt>();

            int M = grid.Length, N = grid[0].Length;

            for(int i=0; i<M; i++)
            {
                listOfStartPos.Add(Tuple.Create(i, -1));
                listOfInitDir.Add(Tuple.Create(0, 1));
                listOfStartPos.Add(Tuple.Create(i, M));
                listOfInitDir.Add(Tuple.Create(0, -1));
            }

            for(int j=0; j <N; j++)
            {
                listOfStartPos.Add(Tuple.Create(-1, j));
                listOfInitDir.Add(Tuple.Create(1, 0));
                listOfStartPos.Add(Tuple.Create(M, j));
                listOfInitDir.Add(Tuple.Create(-1, 0));
            }

            for(int i=0; i<listOfStartPos.Count; i++)
            {
                var startPos = listOfStartPos[i];
                var initDir = listOfInitDir[i];

                var res = Simulate(grid, startPos, initDir);
                listOfRes.Add(res);
            }

            return listOfRes.Max();
        }
    }
}
