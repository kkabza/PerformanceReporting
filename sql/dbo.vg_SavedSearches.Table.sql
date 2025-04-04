USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_SavedSearches]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_SavedSearches](
	[SearchID] [int] IDENTITY(730,1) NOT NULL,
	[UserID] [uniqueidentifier] NULL,
	[SearchName] [varchar](30) NULL,
	[SearchCriteria] [varchar](500) NULL,
	[VGProductID] [int] NULL,
 CONSTRAINT [PK_vg_SavedSearches] PRIMARY KEY CLUSTERED 
(
	[SearchID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
