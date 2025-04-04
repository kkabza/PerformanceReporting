USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_SearchCriteria]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_SearchCriteria](
	[SearchCriteriaID] [int] IDENTITY(1,1) NOT NULL,
	[SearchType] [varchar](20) NULL,
	[ColumnDescription] [varchar](50) NULL,
	[TableColumn] [varchar](50) NULL,
	[TableName] [varchar](50) NULL,
	[SearchGroup] [int] NULL,
 CONSTRAINT [PK_VG_SearchCriteria] PRIMARY KEY CLUSTERED 
(
	[SearchCriteriaID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
